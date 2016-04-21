# -*- coding: utf-8 -*-

# Needed to generate a UUID in index()
from gluon import utils as gluon_utils

# Needed to slow down time in load_devices()
import time
import datetime

proc_table = db.procedures
revisions_table = db.procedure_revisions

def get_procedure_data(procedure_id, stable):
    """
    Returns actual code that corresponds to a given procedure ID.
    Returns either the most recent stable version or the most recent absolute version.

    :param procedure_id: Procedure ID for which code should be fetched
    :type procedure_id: long
    :param stable: Flag that determines whether the code returned should be most recent stable or just the most recent
    :type stable: bool
    :return: Data stored for the procedure
    :rtype: str
    """

    # Get the most recent date, either stable or absolute
    max = revisions_table.last_update.max()
    if stable:
        date = db((revisions_table.procedure_id == procedure_id) &
                  (revisions_table.stable_version == stable)).select(max).first()[max]
    else:
        date = db(revisions_table.procedure_id == procedure_id).select(max).first()[max]

    # Return the data corresponding the procedure ID and determined date
    return db((revisions_table.procedure_id == procedure_id) &
              (revisions_table.last_update == date)).select(revisions_table.procedure_data).first().procedure_data


def save(procedure_id, procedure_data, stable):
    """
    Save code corresponding to a procedure ID as either a stable version or a temporary version

    :param procedure_id: Procedure ID for which code should be fetched
    :type procedure_id: long
    :param procedure_data: Code that should be saved
    :type procedure_data: str
    :param stable: Flag that determines whether the code should be sent to client on next request or not
    :type stable: bool
    """

    # Insert new record to revisions table
    revisions_table.insert(procedure_id = procedure_id,
                           procedure_data = procedure_data,
                           last_update = datetime.datetime.utcnow(),
                           stable_version = stable)

    # Only keep temporary revisions until next stable revision comes in
    # Clean up old temporary revisions upon stable save
    if stable:
        db((revisions_table.procedure_id == procedure_id) &
           (revisions_table.stable_version == False)).delete()

def get_procedures_for_user(user_id, device_id):
    """
    This function returns all procedure IDs that are associated with a given user

    :param user_id: User id associated with the account that is trying to access their procedures
    :type user_id: str
    :return: List of procedure IDs associated with user_id
    :rtype:
    """

    # Get all relevant records for user_id
    records = db((proc_table.user_id == user_id) &
                 (proc_table.device_id == device_id)).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        procedure_ids.append(row.id)

    return procedure_ids


def index():
    """
    Description: Controller for the home page.
    Returns: a redirect to the splash page if not logged in or a list of the devices + UUID to index.html if you are.
    """
    # just throwing some code in here to test proc harness

    db(proc_table).delete()
    db(revisions_table).delete()
    proc_id = create_procedure("blah", "blah@blah")
    save(proc_id, "blahblah", True)

    proc_id2 = create_procedure("blah2", "blah2@blah")
    save(proc_id2, "blahblah2", False)

    save(proc_id2, "blahblah3", False)

    #for row in db(proc_table).select(): 
    #    print row.id, row.user_id, row.name  
    # #for row in db(revisions_table).select(): 
    #    print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

    proc_list1 = get_procedures_for_user("blah@blah")
    proc_list2 = get_procedures_for_user("blah2@blah")

    for row in db(revisions_table).select():  
        print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

    print "first", get_procedure_data(proc_list1[0], True)
    print "second", get_procedure_data(proc_list2[0], False)

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
