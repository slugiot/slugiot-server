# -*- coding: utf-8 -*-

"""
time: Used to slow down loading in load_devices()
access: Used for permission management when adding procedure
gluon_utils: Used to generate UUID passed to index for signature
proc_harness_module: Used for adding procedures
"""
from gluon import utils as gluon_utils
import time
import access
import proc_harness_module
import datetime
import random


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
    Returns (if not logged in): a redirect to the splash page.
    Returns (if logged in): A list of all the devices that are associated with your email (and a UUID for signatures)
    """
    # Redirect to splash page if not logged in
    if auth.is_logged_in() is False:
        redirect(URL('default', 'login.html'))
        response.ptype = 'share'
        response.device_name = "Try"
        return dict(message=T('Please sign in!'))
    else:
        # Generate a UUID for user signatures
        sign_uuid = gluon_utils.web2py_uuid()

        # Generate a list of device associated with the user's email address.
        device_list = db(db.device.user_email == auth.user.email).select()

        # Return the list of devices and UUID
        response.device_name = "Cat"
        return dict(device_list=device_list, sign_uuid=sign_uuid)


def login():
    """
    Description: Controller for the login/splash page.
    Returns: Nothing of substance
    """
    if auth.is_logged_in() is True:
        redirect(URL('default', 'index'))
    return dict()


@auth.requires_login()
@auth.requires_signature()
def new_device():
    device = db.device[request.args(0)]
    db.device.user_email.readable = False
    form = SQLFORM(db.device, record=device, readonly=True)
    if form.process().accepted:
        session.flash = T(form.vars.name + ' added!')
        redirect(URL('default', 'manage', vars=dict(device=device.id)))
    return dict(form=form)


def modal():
    foo = "foo!"
    return dict(fo3o=foo)


@auth.requires_login()
def add_new_procedure():
    """
    Description: Controller for the add page, which lets you add a device into the DB.
    Returns: A form that lets you add things into db.devices (use by including {{=form}})
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
        name = db(db.device.device_id == val).select()[0].name + "_procedure"

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
    form.custom.widget.name['requires'] = IS_NOT_EMPTY()
    if form.process().accepted:
        session.flash = T('Device edited')
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def manage():
    """
    Controller for the procedure manager page. Parses the device ID and returns a list of procedures
    that are associated with the device ID.
    :return: procedure_list, uuid, and vars for URL
    """
    # Extract the device ID from the URL
    device_id = request.vars['device']

    # Go back if there's no device ID for some reason
    # TODO: Also ensure that the device ID is actually in the database.
    if device_id is None:
        session.flash = T('Device not found.')
        redirect(URL('default', 'index'))

    # Generate a UUID for user signature
    sign_uuid = gluon_utils.web2py_uuid()

    # Find all the procedures for this device
    procedure_list = db(db.procedures.device_id == device_id).select()

    # Return the procedure list, UUID, and device ID (as val) to be used in the page.
    return dict(procedures_list=procedure_list, sign_uuid=sign_uuid, val=device_id)


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
    # if procedure_id or stable is None:
    # session.flash = T('No such ID')
    # redirect(URL('default', 'index'))
    return dict(procedure_id=procedure_id, stable=stable)


@auth.requires_login()
def load_devices():
    """
    Description: Returns a list of devices to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the devices and their database fields.
    """
    rows = db(db.device.user_email == auth.user.email).select()
    d = {r.id: {'name': r.name,
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
    if request.args(0) == 'profile':
        db.auth_user.email.writable = False
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


@auth.requires_login()
def share():
    return dict()


"""
---------------------------  Visualization ---------------------------
"""


def test_fill(device_id):
    """Fills some data for visualization."""
    procedure_id = 12580
    name = "cpp03"
    # Clear previous data.
    db(db.outputs).delete()
    db(db.logs).delete()
    print "111111"
    # fill some data for module_values table
    db(db.module_values).delete()
    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            output_value="egg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            output_value="leg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    print "22222"
    for i in range(5):
        db.outputs.insert(device_id=device_id,
                          procedure_id=procedure_id,
                          name=name,
                          time_stamp=now - datetime.timedelta(days=i) - datetime.timedelta(hours=i),
                          output_value=random.random() * 20,
                          tag="1")
        db.logs.insert(device_id=device_id,
                       procedure_id=procedure_id,
                       time_stamp=now - datetime.timedelta(days=i),
                       log_level=random.randint(0, 4),
                       log_message='This is message' + str(i) + '.')
    print "333333"


def fill_device(device_id):
    db(db.procedure_revisions).delete()
    db.procedure_revisions.insert(procedure_id=10086,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    db.procedure_revisions.insert(procedure_id=12580,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    # db(db.device).delete()
    db.device.insert(device_id=device_id,
                     user_email='admin@google.com',
                     name='admin'
                     )
    db(db.procedures).delete()
    db.procedures.insert(device_id=device_id,
                         name='app01'
                         )
    db.procedures.insert(device_id=device_id,
                         name='bpp02'
                         )
    db.procedures.insert(device_id=device_id,
                         name='cpp03'
                         )


# @auth.requires_signature()
def get_modulename():
    device_id = request.vars.device_id
    modulename = []
    for row in db(db.module_values.device_id == device_id).select():
        modulename.append(row.procedure_id)
    print modulename
    print "end of get_modulename"
    result = {'module_name': modulename}
    return response.json(result)


def get_parameter():
    id = request.vars.device_id

    record = db(db.device.id == id).select().first()
    print record.device_id

    fill_device(record.device_id)
    print 'finish adding device info'
    name = []
    procedure_id = []

    for row in db(db.procedures.device_id == record.device_id).select():
        name.append({'name': row.name})

    for row in db(db.procedure_revisions).select():
        procedure_id.append({'procedure_id': row.procedure_id})

    result = {'name': name, 'procedure_id': procedure_id}
    return response.json(result)


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """
    # date1
    s = request.vars.start
    # date2
    e = request.vars.end
    # device_id
    record = db(db.device.id == request.vars.device_id).select().first()
    device_id = record.device_id
    print "??????????????????????"
    print device_id
    # module_name or procedure_id
    procedure_id = request.vars.procedure_id
    # name
    name = request.vars.name

    # parse the start date and end date
    start_year = int(s[0:4])
    start_month = int(s[5:7])
    start_day = int(s[8:10])
    start_hour = int(s[11:13])
    start_minute = int(s[14:16])
    start_second = int(s[17:19])

    end_year = int(e[0:4])
    end_month = int(e[5:7])
    end_day = int(e[8:10])
    end_hour = int(e[11:13])
    end_minute = int(e[14:16])
    end_second = int(e[17:19])

    # print 111111111111111111111111
    # transform the start date and end date into datetime format
    start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
    end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)

    print "before test_fill"
    test_fill(device_id)

    print "----------finish test fill-----------------------"
    # get output_data and sort by time_stamp
    output_data = db((db.outputs.time_stamp >= start) &
                     (db.outputs.time_stamp <= end) &
                     (db.outputs.device_id == device_id) &
                     (db.outputs.procedure_id == procedure_id) &
                     (db.outputs.name == name)).select(orderby=db.outputs.time_stamp)
    # get log_data and sort by time_stamp
    log_data = db((db.logs.time_stamp >= start) &
                  (db.logs.time_stamp <= end) &
                  (db.logs.device_id == device_id) &
                  (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.time_stamp)
    # generate mixed_data from output_data and log_data and sort by time_stamp
    mixed_data = []
    # transform output_data into mixed_data
    for row in db((db.outputs.time_stamp >= start) &
                          (db.outputs.time_stamp <= end) &
                          (db.outputs.device_id == device_id) &
                          (db.outputs.procedure_id == procedure_id) &
                          (db.outputs.name == name)).select(orderby=db.outputs.time_stamp):
        type = 'output'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.time_stamp
        name = row.name
        value = row.output_value
        tag = row.tag
        content = 'name: ' + str(name) + ', value: ' + str(value) + ', tag: ' + str(tag)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
    print 111111111111111111111111
    # transform log_data into mixed_data
    for row in db((db.logs.time_stamp >= start) &
                          (db.logs.time_stamp <= end) &
                          (db.logs.device_id == device_id) &
                          (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
    print 111111111111111111111111
    # sort the mixed_data by time_stamp
    mixed_data.sort(key=lambda r: r['time_stamp'])
    # build the return data in dict format
    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}
    # dump into json format
    return response.json(result)


def viz():
    # storage device_id, and module in session for testing (fake)
    # later need to read them from UI backend
    # session.device_id = "chicken"
    # session.module = ["egg", "eggnog"]
    # return dict(session=session)
    result = -1
    if len(request.args) > 0:
        result = request.args[0]
    return {"device_id": result}
