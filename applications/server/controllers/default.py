# -*- coding: utf-8 -*-

"""
time: Used to slow down loading in load_devices()
access: Used for permission management when adding procedure
gluon_utils: Used to generate UUID passed to index for signature
proc_harness_module: Used for adding procedures
"""
from gluon import utils as gluon_utils
import time, access, proc_harness_module


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
        device_list = db(db.device.user_email == auth.user.email).select()
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
def add_procedure():
    db = current.db
    proc_table = db.procedures
    revisions_table = db.procedure_revisions
    db(proc_table).delete()
    db(revisions_table).delete()

    # set logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # add permission for the user management
    access.add_permission("1", auth.user.email, perm_type="a")

    # create procedure name=demo_1 for the device whose id = 1 and saved it
    proc_id = proc_harness_module.create_procedure("demo_1", "1")
    proc_harness_module.save(proc_id, "# This is your new (stable) procedure. Happy coding!", True)
    time.sleep(2)
    proc_harness_module.save(proc_id, "This is your new (temporary) procedure. Happy coding!", False)
    time.sleep(2)

    return "ok"


@auth.requires_login()
def load_devices():
    # TODO: Condense "rows" to just for that one specific user instead of ALL devices
    """
    Description: Returns a list of devices to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the devices and their database fields.
    """
    rows = db(db.device.user_email == auth.user.email).select()
    time.sleep(1)  # so we can some time to stare at the pretty animation :-)
    d = {r.device_id: {'name': r.name,
                       'description': r.description,
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


def manage():
    device_id = request.args(0)
    s = SHOP_LIST.get(sid)
    logger.info("Found the store: %r" % s)
    if s is None:
        session.message = T('No such store')
        redirect(URL('default', 'index'))
    session.pasta_sauce = "Pesto"  # Not used.
    return dict(shop=s)


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
