# -*- coding: utf-8 -*-

"""
time: Used to slow down loading in load_devices()
access: Used for permission management when adding procedure
gluon_utils: Used to generate UUID passed to index for signature
proc_harness_module: Used for adding procedures
"""
from gluon import utils as gluon_utils
import time, access, proc_harness_module


class DeviceIDVerification:
    """
    This is used for device edits. Accepts device ID as an argument.
    Returns: The web2py table ID for the particular device.
    """
    def __init__(self, error_message='Could not verify device'):
        self.e = error_message

    def __call__(self, device_id):
        if db(db.device.device_id == device_id).select():
            return db(db.device.device_id == device_id).select()[0].id
        return device_id


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
        device_id = form.vars.device_id
        access.add_permission(user_email=auth.user.email, perm_type='a', device_id=device_id)
        session.flash = "Device added!"
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def add_new_procedure():
    """
    Description: Controller for the add page, which lets you add a device into the DB.
    Returns: A form that lets you add things into db.devices (use by including {{=form}} in add.html)
    """
    # Device ID should not be changeable
    db.procedures.device_id.writable = False
    val = request.vars['device']
    if val is None:
        session.flash = T('No such device')
        redirect(URL('default', 'index'))
    else:
        db.procedures.device_id.default = val
    form = SQLFORM(db.procedures)

    # set the logger logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # initialize name variable
    name = ""

    # Generate a name to be passed on to add_permission
    if db(db.device.device_id == val).select():
        name = db(db.device.device_id == val).select()[0].name + " procedure"

    if form.process().accepted:

        proc_id = proc_harness_module.create_procedure(name, val)
        # Initialize some starter Python code
        proc_harness_module.save(proc_id, "#This is your new (stable) procedure. Happy coding!", True)
        # Sleep a little bit to allow it to successfully save
        time.sleep(2)
        # Initalize the draft Python ocde as well
        proc_harness_module.save(proc_id, "#This is your new (temporary) procedure. Happy coding!", False)
        # Sleep a little bit again
        time.sleep(2)
        # Go back to the home page.
        session.flash = "Procedure added!"
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def edit_device():
    """
    Controller for the page that lets you edit a device.
    :return: a form
    """
    val = request.vars['device']
    table_id = DeviceIDVerification().__call__(val)
    if table_id is None:
        session.flash = T('No such device')
        redirect(URL('default', 'index'))
    form = SQLFORM(db.device, record=int(table_id))
    if form.process().accepted:
        session.flash = T('Device edited')
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def manage():
    """
    Controller for the procedure manager page.
    :return: procedure_list, uuid, and vars for URL
    """
    val = request.vars['device']
    sign_uuid = gluon_utils.web2py_uuid()
    procedure_list = db(db.procedures.device_id == val).select()
    return dict(procedures_list=procedure_list, sign_uuid=sign_uuid, val=val)


@auth.requires_login()
def edit_procedure():
    """
    Description: Passed procedure ID and stability mode to the editor to use
    :return: procedure_id and stable
    """
    # get the procedure_id and stable statues of procedure in TABLE procedure
    procedure_id = int(request.vars['procedure_id'])
    stable = request.vars['stable']
    print stable
    #if procedure_id or stable is None:
        #session.flash = T('No such ID')
        # redirect(URL('default', 'index'))
    return dict(procedure_id=procedure_id, stable=stable)


@auth.requires_login()
def load_devices():
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
def read_procedures():
    """
    Description: Returns a list of devices to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the devices and their database fields.
    """
    val = request.vars['device']
    rows = db(db.procedures.device_id == val).select()
    time.sleep(1)  # so we can some time to stare at the pretty animation :-)
    d = {r.device_id: {'name': r.name,
                       'id': r.id}
         for r in rows}
    return response.json(dict(procedure_dict=d))


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
