import datetime
import access
import unittest

import time
import os
from gluon import current, DAL, Field
from gluon.tools import Auth

#auth = Auth(globals(), current.db)

####### API FOR EDITOR TEAM ##########

#@auth.requires_login()
def create_procedure(procedure_name, device_id):
    """
    This function should be called when a new procedure is created in the editor.

    :param procedure_name: Name of the new procedure
    :type procedure_name: str
    :param device_id: Device ID associated with device on which user wants to create proc
    :type device_id: str
    :return: ID associated with new procedure (procedure_id in revisions table)
    :rtype: long
    """
    db = current.db
    auth = Auth(globals(), db)
    proc_table = db.procedures

    user_email = "blah@blah.com"

    if not access.can_create_procedure(device_id, user_email):
        print "YOOOOOOOOO DAWG"
        return None

    pid = proc_table.insert(device_id = device_id, name = procedure_name)
    access.add_permission(device_id = device_id, user_email = user_email, procedure_id = pid)
    return pid

#@auth.requires_login()
def get_procedures_for_edit(device_id):
    """
    This function returns all procedure IDs that are associated with a given user to edit

    :param device_id: Device ID associated with device on which user wants to create proc
    :type device_id: str
    :return: List of procedure IDs associated with device
    :rtype:
    """
    db = current.db
    auth = Auth(globals(), db)
    proc_table = db.procedures

    user_email = "blah@blah.com"

    # Get all relevant records for user_email
    records = db(proc_table.device_id == device_id).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        if access.can_edit_procedure(user_email, device_id, row.id):
            procedure_ids.append(row.id)

    return procedure_ids

#@auth.requires_login()
def get_procedures_for_view(device_id):
    """
    This function returns all procedure IDs that are associated with a given user to view ONLY

    :param device_id: Device ID associated with device on which user wants to create proc
    :type device_id: str
    :return: List of procedure IDs associated with device
    :rtype:
    """

    db = current.db
    auth = Auth(globals(), db)
    proc_table = db.procedures

    # Get all relevant records for user_email
    user_email = auth.user.email
    records = db(proc_table.device_id == device_id).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        if (not access.can_edit_procedure(user_email, device_id, row.id)) and\
                access.can_view_procedure(user_email, device_id, row.id):
            procedure_ids.append(row.id)

    return procedure_ids


def __get_most_recent_date__(procedure_id, is_stable):
    db = current.db
    revisions_table = db.procedure_revisions

    # Get the most recent date, either stable or absolute
    max = revisions_table.last_update.max()
    if is_stable:
        date = db((revisions_table.procedure_id == procedure_id) &
                  (revisions_table.is_stable == is_stable)).select(max).first()[max]
    else:
        date = db(revisions_table.procedure_id == procedure_id).select(max).first()[max]

    return date


#@auth.requires_login()
def get_procedure_data(procedure_id, is_stable):
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

    db = current.db
    revisions_table = db.procedure_revisions

    date = __get_most_recent_date__(procedure_id, is_stable)

    # Return the data corresponding the procedure ID and determined date
    return db((revisions_table.procedure_id == procedure_id) & (revisions_table.last_update == date)).select(revisions_table.procedure_data).first().procedure_data

#@auth.requires_login()
def get_procedure_name(procedure_id):
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

    db = current.db
    proc_table = db.procedures

    # Return the data corresponding the procedure ID and determined date
    return db(proc_table.id == procedure_id).select(proc_table.name).first().name


#@auth.requires_login()
def save(procedure_id, procedure_data, is_stable):
    """
    Save code corresponding to a procedure ID as either a stable version or a temporary version

    :param procedure_id: Procedure ID for which code should be fetched
    :type procedure_id: long
    :param procedure_data: Code that should be saved
    :type procedure_data: str
    :param stable: Flag that determines whether the code should be sent to client on next request or not
    :type stable: bool
    """

    db = current.db
    revisions_table = db.procedure_revisions

    # Insert new record to revisions table
    revisions_table.insert(procedure_id = procedure_id,
                           procedure_data = procedure_data,
                           last_update = datetime.datetime.utcnow(),
                           is_stable = is_stable)

    # Only keep temporary revisions until next stable revision comes in
    # Clean up old temporary revisions upon stable save
    if is_stable:
        db((revisions_table.procedure_id == procedure_id) &
           (revisions_table.is_stable == False)).delete()


####################### TEST CODE #######################

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

    print "hey"

    # add permission for the usermanagement
    access.add_permission("1","blah@blah.com",perm_type="a")

    # create procedure name=demo_1 for the device whose id = 1 and saved it
    proc_id = create_procedure("demo_1", "1")
    print "proc_id", proc_id, type(proc_id)
    save(proc_id, "#demo1 stable edition code", True)
    time.sleep(2)
    save(proc_id, "#demo1 temporary edition code", False)
    time.sleep(2)
    # create procedure name=demo_2 for the device whose id = 1 and saved it
    proc_id2 = create_procedure("demo_2", "1")
    save(proc_id2, "#demo2 stable edition code", True)
    time.sleep(2)
    save(proc_id2, "#demo2 temporary edition code", False)

    # get the list of procedure_id from device whose id = 1
    proc_list1 = get_procedures_for_edit("1")
    proc_list2 = get_procedures_for_edit("1")

    # get the data of procedure
    data1 = get_procedure_data(proc_list1[0], True)
    data2 = get_procedure_data(proc_list2[0], False)
    return "ok"

class TestProcedureHarness(unittest.TestCase):
    def setUp(self):
        #os.system("rm -rf ../testdatabases")
        try:
            os.remove("../testdatabases")
        except:
            pass
        pdir = os.getcwd()
        os.system("cp -r ../databases ../testdatabases")
        #os.system("python ../../../scripts/cpdb.py -f ../databases -F ../testdatabases -y 'sqlite://storage.sqlite' -Y 'sqlite://storage.sqlite' -d ../../../gluon")
        # This approach won't work for GAE because it isn't using SQLite.
        current.db = DAL('sqlite://storage.sqlite', folder = '../testdatabases/',
                      pool_size="10",
                      migrate_enabled="true",
                      check_reserved=['all']
                      )
        self.db = current.db
        db = self.db
        # The database will be empty until we populate it with table structure
        filename = "../models/tables.py"
        with open(filename, 'rb+') as tables_code:
            exec(tables_code.read())
        print "tables!!", self.db.tables
        self.proc_table = self.db.procedures
        self.revisions_table = self.db.procedure_revisions

        access.add_permission("test", "test@test.com", perm_type="a")

    #@unittest.skip("later")
    def testBasicFlow(self):
        proc_id = create_procedure("blah", "blah@blah", "test")
        save(proc_id, "blahblah", True)
        proc_id2 = create_procedure("blah2", "blah2@blah", "test")
        save(proc_id2, "blahblah2", True)
        time.sleep(2)
        save(proc_id2, "blahblah3", False)

        proc_list1 = get_procedures_for_edit("test")

        val1 = get_procedure_data(proc_list1[0], True)
        val2 = get_procedure_data(proc_list1[0], False)

        val3 = get_procedure_data(proc_list1[1], True)
        val4 = get_procedure_data(proc_list1[1], False)

        self.assertEqual("blahblah", val1)
        self.assertEqual("blahblah", val2)
        self.assertEqual("blahblah2", val3)
        self.assertEqual("blahblah3", val4)

#if __name__ == '__main__':
#    unittest.main() # runs all unit tests