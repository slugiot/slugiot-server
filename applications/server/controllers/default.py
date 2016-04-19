# -*- coding: utf-8 -*-

from gluon import utils as gluon_utils
import time


def index():
    """
    Controller for the home page.
    Returns SQLFORM of devices if logged in and a list of all the devices.
    """
    sign_uuid = gluon_utils.web2py_uuid()
    if auth.user_id is None:
        # Would sign_uuid really be needed here? Leaving just in case.
        return dict(message=T('Please sign in!'), sign_uuid=sign_uuid)
    else:
        device_list = db().select(db.devices.ALL)
        return dict(device_list=device_list, sign_uuid=sign_uuid)


@auth.requires_login()
def add():
    db.devices.device_id.writable = True
    db.devices.last_sync.readable = db.devices.last_sync.writable = False
    form = SQLFORM(db.devices)
    if form.process().accepted:
        session.flash = "Device added!"
        redirect(URL('default', 'index'))
    return dict(form=form)


def load_devices():
    # TODO: Condense "rows" to just for that one specific user instead of ALL devices
    rows = db(db.devices).select()
    time.sleep(1)  # so we can some time to stare at the pretty animation :-)
    d = {r.device_id: {'name': r.name,
                       'description': r.description,
                       'device_icon': r.device_icon,
                       'user_email': r.user_email,
                       'id': r.id}
         for r in rows}
    return response.json(dict(device_dict=d))


@auth.requires_signature()
def delete_devices():
    delete_devices = request.vars.get("delete_devices[]")
    if type(delete_devices) is str:
        db(db.devices.device_id == delete_devices).delete()
    else:
        for i in delete_devices:
            db(db.devices.device_id == i).delete()
    return "ok"


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
