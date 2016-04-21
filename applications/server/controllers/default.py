# -*- coding: utf-8 -*-

# Needed to generate a UUID in index()
from gluon import utils as gluon_utils

# Needed to slow down time in load_devices()
import time


def index():
    """
    Description: Controller for the home page.
    Returns: a redirect to the splash page if not logged in or a list of the devices + UUID to index.html if you are.
    """
    if auth.user_id is None:
        redirect(URL('default', 'login.html'))
        return dict(message=T('Please sign in!'))
    else:
        sign_uuid = gluon_utils.web2py_uuid()
        device_list = db().select(db.device.ALL)
        return dict(device_list=device_list, sign_uuid=sign_uuid)


def login():
    """
    Description: Controller for the login/splash page.
    Returns: Nothing of substance
    """
    return dict(message=T('Welcome to SlugIOT!'))


@auth.requires_login()
def add():
    """
    Description: Controller for the add page, which lets you add a device into the DB
    Returns: A form that lets you add things into db.devices (use by including {{=form}} in add.html)
    """
    db.device.device_id.writable = True
    form = SQLFORM(db.device)
    if form.process().accepted:
        session.flash = "Device added!"
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def load_devices():
    # TODO: Condense "rows" to just for that one specific user instead of ALL devices
    """
    Description: Returns a list of devices to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the devices and their database fields.
    """
    rows = db(db.device).select()
    time.sleep(1)  # so we can some time to stare at the pretty animation :-)
    d = {r.device_id: {'name': r.name,
                       'description': r.description,
                       'device_icon': r.device_icon,
                       'user_email': r.user_email,
                       'id': r.id}
         for r in rows}
    return response.json(dict(device_dict=d))


@auth.requires_login()
@auth.requires_signature()
def delete_devices():
    # TODO: Rename delete_devices so it doesn't shadow the name from an outer scope
    """
    Description: Deletes items from the device database using the device ID.
    Returns: An "ok" so you know the deletion is done.
    """
    delete_devices = request.vars.get("delete_devices[]")
    if type(delete_devices) is str:
        db(db.device.device_id == delete_devices).delete()
    else:
        for i in delete_devices:
            db(db.device.device_id == i).delete()
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
