
# -*- coding: utf-8 -*-
# this file is used to test the editor

import proc_harness_module
from datetime import datetime
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
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}

    # get the procedure_id and stable state of procedure in TABLE procedure
    device_id = request.vars['device_id']
    procedure_id = request.vars['procedure_id']
    stable = request.vars['stable']
    # the final edition will use Team 2 API "get_procedure_data(procedure_id, stable)"  to get the data
    #data = db(db.coding.id == procedure_id).select(db.coding.procedures).first().procedures
    if stable == 'false':
        data = proc_harness_module.get_procedure_data(procedure_id, False)
    else:
        data = proc_harness_module.get_procedure_data(procedure_id, True)

    # get the list of procedure_id belongs to the device
    proc_list = proc_harness_module.get_procedures_for_edit(device_id)
    #TO DO change the API to proc_harness_module.get_procedures_name_for_edit(device_id)
    proc_name_list = proc_harness_module.get_procedures_for_edit(device_id)
    file_details = dict(
                    editor_settings=preferences,     # the option parameters used for setting editor feature.
                    id=procedure_id,                 # the procedure_id in the procedures TALBE
                    data=data,                       # code for procedure which is related with the id.
                    dev_id = device_id,              # id of the device
                    id_list = proc_list,              # id list of procedure belong to the device
                    name_list = proc_name_list       # name list of the procedure belong to the device
                    )

    # generated HTML code for editor by parameters in file_details
    plain_html = response.render('editor/edit_js.html', file_details)

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

    #save the procedure data to the database
    if stable == 'false':

        #the final edition will use Team 2 API save(procedure_id, stable) to save the temporary procedure
        #db(db.coding.id == procedure_id).update(procedures = data)
        proc_harness_module.save(procedure_id,data,False)

    else:
        # compile the stable procedure and saved it if there is no exception during compiling

        import _ast
        try:
            code = request.vars.procedure.rstrip().replace('\r\n', '\n') + '\n'
            compile(code, '<string>', "exec", _ast.PyCF_ONLY_AST)

            #the final edition will use Team 2 API save(procedure_id, stable) to save the data
            #db(db.coding.id == procedure_id).update(procedures = data)
            proc_harness_module.save(procedure_id,data,True)

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

    file_save = dict(result = result_html,
                     highlight = highlight)
    return response.json(file_save)

# @auth.requires_signature()
def delete_procedure():
    """
    This function is used to delete specific procedure
    :return:
    """
    procedure_id = request.vars.procedure_id
    device_id = request.vars.device_id
    proc_harness_module.delete_procedure(procedure_id,device_id)
    redirect(URL('default', 'index'))



## all the following function is used for self debug and will be deleted at final edition
def create():
    """
    This function is only used for self debug to create a new procedure and will be deleted in the final edition
    Team 2 provide the API create_procedure() to create a new procedure and return the procedure_id

    :return: the time for create one row in database
    :rtype: str
    """

    # get the utc time for the create process
    now = datetime.utcnow()

    # the initial procedure data that saved for this row
    code = "# enter your new procedure in the following" + now.strftime("%Y-%m-%d %H:%M:%S")

    # insert a new row for procedure
    db.coding.insert(procedures=code, times=now)

    return dict(result = now)


def select():
    """
    This function is only used for self debug to show exited procedure in database and will be deleted in the final edition
    Team 2 provide the API get_procedures_for_user(user_id) to return the list of procedure_id belong to a user

    :return: the existed rows for procedure in database
    :rtype: dict
    """

    return dict(code_list = db(db.coding).select())


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
    device_id = request.vars.device_id
    procedure_id = request.vars.procedure_id
    stable = request.vars.stable
    return dict(device_id = device_id, procedure_id = procedure_id, stable=stable)

def eprint():
    print('ok')



def run_test():
    """
    test code refered and edited from proc_harness_module.py
    this is only used for demo in the next class and will be deleted later
    :return:
    """
    import access
    import time
    db = current.db
    proc_table = db.procedures
    revisions_table = db.procedure_revisions
    db(proc_table).delete()
    db(revisions_table).delete()

    #set logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # add permission for the usermanagement
    access.add_permission("1","blah@blah.com",perm_type="a")

    # create procedure name=demo_1 for the device whose id = 1 and saved it
    proc_id = proc_harness_module.create_procedure("demo_1", "1")
    proc_harness_module.save(proc_id, "#demo1 stable edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered", True)
    time.sleep(2)
    proc_harness_module.save(proc_id, "#demo1 temporary edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered", False)
    time.sleep(2)
    # create procedure name=demo_2 for the device whose id = 1 and saved it
    proc_id2 = proc_harness_module.create_procedure("demo_2", "1")
    proc_harness_module.save(proc_id2, "#demo2 stable edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered", True)
    time.sleep(2)
    proc_harness_module.save(proc_id2, "#demo2 temporary edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered", False)

    # get the list of procedure_id from device whose id = 1
    proc_list1 = proc_harness_module.get_procedures_for_edit("1")
    proc_list2 = proc_harness_module.get_procedures_for_edit("1")
    logger.info(proc_list1)

    # get the data of procedure
    data1 =proc_harness_module.get_procedure_data(proc_list1[0], True)
    logger.info(data1)
    data2 =proc_harness_module.get_procedure_data(proc_list2[0], False)
    logger.info(data2)
    return "ok"

def unit_test():
    """
    generate the page for selenium unit test
    :return:
    """
    # get the procedure_id list for device 1
    id_list = proc_harness_module.get_procedures_for_edit("1")
    return dict(id_list=id_list)