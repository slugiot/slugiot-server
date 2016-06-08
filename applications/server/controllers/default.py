# -*- coding: utf-8 -*-

"""
time: Used to slow down loading in load_devices()
access: Used for permission management when adding procedure
gluon_utils: Used to generate UUID passed to index for signature
proc_harness_module: Used for adding procedures
"""
from gluon import utils as gluon_utils

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
        # Return the list of devices and UUID
        val1 = request.vars['device_id']
        if val1 is not None:
            val = db(db.device.id == val1).select()[0].name
            response.device_name = val
        return dict()


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
    access.add_permission(user_email=auth.user.email, perm_type='a', device_id=device.device_id)
    if form.process().accepted:
        session.flash = T(form.vars.name + ' added!')
        redirect(URL('default', 'manage', vars=dict(device=device.id)))
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
def load_exist_procedures():
    """
    Description: Returns a list of devices to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the devices and their database fields.
    """
    val = int(request.vars['device_id'])
    if val is not None:
        print "Test Record "
        print val
    device_id = db(db.device.id == val).select()[0].device_id
    print device_id

    # get the list of procedure_id belongs to the device
    proc_list = proc_harness_module.get_procedures_for_edit(device_id)
    # TO DO change the API to proc_harness_module.get_procedures_name_for_edit(device_id)
    proc_name_list = proc_harness_module.get_procedures_name_for_edit(device_id)
    # for proc_id in proc_list:
    #    d['id'] = proc_id
    d = []
    for i in range(len(proc_list)):
        d.append(dict(name=proc_name_list[i], id=proc_list[i]))
    # d = dict(zip(proc_list, proc_name_list))
    if d is not None:
        print "Is this none?"
    # dic = dict(zip(proc_list, d))
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

    val1 = request.vars['device_id']
    if val1 is not None:
        val = db(db.device.id == val1).select()[0].name
        response.device_name = val

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
    val1 = request.vars['device_id']
    if val1 is not None:
        val = db(db.device.id == val1).select()[0].name
        response.device_name = val

    return dict()


"""
---------------------------  Visualization ---------------------------
"""


# @auth.requires_signature()
def get_modulename():
    device_id = request.vars.device_id
    modulename = []
    for row in db(db.module_values.device_id == device_id).select():
        modulename.append(row.procedure_id)
    print modulename
    print "end of get_modulename"
    modulename = set(modulename)
    result = {'module_name': modulename}
    return response.json(result)


def get_parameter():
    """
    Description: Run this function when the procedure id is chosen in the data visualization control panel.
    Returns: A JSON with all the var names belongs to the specific <device id, procedure id> pair from module_values database.
    """
    """
    Description: Run this function when the device id is chosen.
    Returns: A JSON with all the procedure ids belongs to the specific device id using the pro_harness_module API.
    """
    id = request.vars.device_id

    record = db(db.device.id == id).select().first()
    print record.device_id

    print "use api"
    device_id = record.device_id
    # get the list of procedure_id belongs to the device using the procedure harness API
    procedure_id_list = proc_harness_module.get_procedures_for_edit(device_id)
    print 'pro_id ------------'
    print procedure_id_list
    print 'finished'
    print 'finish adding device info'
    name = []
    for row in db(db.procedures.device_id == record.device_id).select():
        name.append({'name': row.name})
    result = {'name': name, 'procedure_id': procedure_id_list}
    return response.json(result)


def get_var_name():
    """
    Description: Excute when the procedure id is chosen in the data visualization control panel.
    Returns: A JSON with all the var names belongs to the specific <device id, procedure id> pair from module_values database.
    """
    id = request.vars.device_id
    procedure_id = request.vars.procedure_id
    record = db(db.device.id == id).select().first()
    device_id = record.device_id
    print 'request data-------------'
    print 'id of the device is :'
    print id
    print 'device id is :'
    print device_id
    print 'procedure id is :'
    print procedure_id
    print '---------'
    print device_id
    print procedure_id
    var_name = []
    for row in db((db.module_values.device_id == device_id) &
                          (db.module_values.procedure_id == procedure_id)).select():
        var_name.append(row.name)
    print '--------return data of get_var_name-----------------'
    print var_name
    var_name = set(var_name)
    print var_name
    result = {'name': var_name}
    return response.json(result)


def get_data():
    """
    Description: Run this function when click the <procedure id, var name> pair in the visualization page.
    Returns: A JSON with all the output information belongs to the specific <device id, procedure id, var name> pair from db.outputs database
             A JSON with all the logs information belongs to the specific <device id, procedure id> pair from db.logs database.
    """
    # date1
    s = request.vars.start
    # date2
    e = request.vars.end
    # device_id
    record = db(db.device.id == request.vars.device_id).select().first()
    device_id = record.device_id
    print device_id
    print '-----------'
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
    print "??????????????????????"

    # print "before test_fill"
    # test_fill(device_id)



    print 'test the query parameter --------------------'
    print device_id
    print name
    print procedure_id

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
    id = request.vars['device_id']
    if id is not None:
        result = id
        response.device_name = db(db.device.id == id).select()[0].name
    return {"device_id": result}


"""
---------------------------  editor_team ---------------------------
"""


# @auth.requires_signature()


def edit_procedure():
    """
    This function received ajax request to generated the HTML content for editor

    : parameter precedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    : type precedure_id: str
    :return: Dict with HTML content of editor and procedure_id, procedure data, editor preferences
    :rtype: Json
    """
    # parameter for CodeMirror option parameter used for setting the editor feature
    preferences = {'theme': 'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth': '4',
                   'indentwithtabs': 'false', 'linenumbers': 'true', 'highlightline': 'true'}

    # get the procedure_id and stable state of procedure in TABLE procedure
    pseudo_id = int(request.vars['device_id'])
    device_id = db(db.device.id == pseudo_id).select()[0].device_id
    procedure_id = request.vars['procedure_id']
    stable = request.vars['stable']
    # the final edition will use Team 2 API "get_procedure_data(procedure_id, stable)"  to get the data
    # data = db(db.coding.id == procedure_id).select(db.coding.procedures).first().procedures
    if stable == 'false':
        data = proc_harness_module.get_procedure_data(procedure_id, False)
    else:
        data = proc_harness_module.get_procedure_data(procedure_id, True)

    # get the list of procedure_id belongs to the device
    proc_list = proc_harness_module.get_procedures_for_edit(device_id)
    # TO DO change the API to proc_harness_module.get_procedures_name_for_edit(device_id)
    proc_name_list = proc_harness_module.get_procedures_name_for_edit(device_id)
    file_details = dict(
        editor_settings=preferences,  # the option parameters used for setting editor feature.
        id=procedure_id,  # the procedure_id in the procedures TALBE
        data=data,  # code for procedure which is related with the id.
        dev_id=pseudo_id,  # id of the sudo device
        id_list=proc_list,  # id list of procedure belong to the device
        name_list=proc_name_list  # name list of the procedure belong to the device
    )

    # generated HTML code for editor by parameters in file_details
    plain_html = response.render('default/edit_js.html', file_details)

    # add the HTML content element for editor to file_details dictionary
    file_details['plain_html'] = plain_html

    return response.json(file_details)


# @auth.requires_signature()
def save_procedure():
    """
    This function received ajax request to save procedure to the procedure TABLE

    : parameter procedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    : type procedure_id: str
    : parameter procedure: the procedure data in procedure TABLE sent by request.vars
    : type procedure: str
    : parameter stable: the sign to identify if saved procedure is stable
    : type stable: str
    :return: whether the procedure is saved correctlly.
    :rtype: str
    """

    # obtain parameter from ajax request
    procedure_id = request.vars.procedure_id
    data = request.vars.procedure
    stable = request.vars.stable

    result_html = DIV(T('file saved successfully'))
    highlight = None

    # save the procedure data to the database
    if stable == 'false':

        # the final edition will use Team 2 API save(procedure_id, stable) to save the temporary procedure
        # db(db.coding.id == procedure_id).update(procedures = data)
        proc_harness_module.save(procedure_id, data, False)

    else:
        # compile the stable procedure and saved it if there is no exception during compiling

        import _ast
        try:
            code = request.vars.procedure.rstrip().replace('\r\n', '\n') + '\n'
            compile(code, '<string>', "exec", _ast.PyCF_ONLY_AST)

            # the final edition will use Team 2 API save(procedure_id, stable) to save the data
            # db(db.coding.id == procedure_id).update(procedures = data)
            proc_harness_module.save(procedure_id, data, True)

        except Exception, e:
            # DISCUSS
            # offset calculation is only used for textarea (start/stop)
            start = sum([len(line) + 1 for l, line
                         in enumerate(request.vars.procedure.split("\n"))
                         if l < e.lineno - 1])

            if e.text and e.offset:
                offset = e.offset - (len(e.text) - len(
                    e.text.splitlines()[-1]))
            else:
                offset = 0
            highlight = {'start': start, 'end': start +
                                                offset + 1, 'lineno': e.lineno, 'offset': offset}
            try:
                ex_name = e.__class__.__name__
            except:
                ex_name = 'unknown exception!'
            result_html = DIV(T('failed to compile and save file because:'), BR(),
                              B(ex_name), ' ' + T('at line %s', e.lineno),
                              offset and ' ' +
                              T('at char %s', offset) or '')

    file_save = dict(result=result_html,
                     highlight=highlight)
    return response.json(file_save)


# @auth.requires_signature()
def delete_procedure():
    """
    This function is used to delete specific procedure
    :return:
    """
    procedure_id = request.vars.procedure_id
    pseudo_id = int(request.vars.device_id)
    device_id = db(db.device.id == pseudo_id).select()[0].device_id
    # call api to delete the procedure
    proc_harness_module.delete_procedure(procedure_id, device_id)
    data = ""
    # response a json type data to redirect to homepage after delete procedure
    return response.json(data=data)


## all the following function is used for self debug and will be deleted at final edition


def test_edit():
    """
    This is served for the test example view page, which help UI team to integrate editor
    This function will be delete at final edition

    parameter procedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    type procedure_id: str
    :return: the procedure_id for procedure in procedure TABLE
    :rtype: dict
    """
    # get the procedure_id and stable statues of procedure in TABLE procedure
    pseudo_id = int(request.vars.device_id)
    device_id = '' + db(db.device.id == pseudo_id).select()[0].device_id
    procedure_id = request.vars.procedure_id
    stable = request.vars.stable

    val1 = request.vars['device_id']
    if val1 is not None:
        val = db(db.device.id == val1).select()[0].name
        response.device_name = val

    return dict(device_id=pseudo_id, procedure_id=procedure_id, stable=stable)
