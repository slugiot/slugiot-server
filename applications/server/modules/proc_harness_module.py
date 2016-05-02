import datetime
import access
import unittest
from gluon import current
from gluon.tools import Auth

auth = Auth(globals(), current.db)

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

    user_email = "blah@blah.com" #auth.auth.user_email

    if not access.can_create_procedure(device_id, user_email):
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

    user_email = "blah@blah.com" #auth.auth.user_email

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
    user_email = "blah@blah.com" #auth.auth.user_email
    records = db(proc_table.device_id == device_id).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        if (not access.can_edit_procedure(user_email, device_id, row.id)) and\
                access.can_view_procedure(user_email, device_id, row.id):
            procedure_ids.append(row.id)

    return procedure_ids



#@auth.requires_login()
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

    db = current.db
    revisions_table = db.procedure_revisions

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

#@auth.requires_login()
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

    db = current.db
    revisions_table = db.procedure_revisions

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


####################### TEST CODE #######################

def run_test():
    db = current.db
    proc_table = db.procedures
    revisions_table = db.procedure_revisions

    print "test1"
    db(proc_table).delete()
    print "test2"
    db(revisions_table).delete()

    access.add_permission("1","blah@blah.com",perm_type="a")

    print "test3"
    proc_id = create_procedure("blah", "1")
    print "test4"
    save(proc_id, "blahblah", True)
    proc_id2 = create_procedure("blah2", "1")
    save(proc_id2, "blahblah2", False)
    save(proc_id2, "blahblah3", False)

    proc_list1 = get_procedures_for_edit("1")
    proc_list2 = get_procedures_for_edit("1")

    print "procs", proc_list1, "two", proc_list2

    for row in db(revisions_table).select():
        print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

    print "first", get_procedure_data(proc_list1[0], True)
    print "second", get_procedure_data(proc_list2[0], False)


class TestProcedureHarness(unittest.TestCase):
    def setUp(self):
        # os.copy('mysafecopy.sql', 'myfile.sql')
        # test_db = DAL('sqlite:myfile.sql')
        # current.db = test_db
        # import mymodule
        # mymodule.foo()

        # eventually want to get db instance of SQL lite and dump database
        self.db = current.db
        self.proc_table = self.db.procedures
        self.revisions_table = self.db.procedure_revisions

        self.db(self.proc_table).delete()
        self.db(self.revisions_table).delete()

    #@unittest.skip("later")
    def testBasicSave(self):
        proc_id = create_procedure("blah", "blah@blah", 1)
        save(proc_id, "blahblah", True)
        proc_id2 = create_procedure("blah2", "blah2@blah", 1)
        save(proc_id2, "blahblah2", False)
        save(proc_id2, "blahblah3", False)

        proc_list1 = get_procedures_for_edit("blah@blah", 1)
        proc_list2 = get_procedures_for_view("blah2@blah", 1)

        for row in self.db(self.revisions_table).select():
            print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

        print "first", get_procedure_data(proc_list1[0], True)
        print "second", get_procedure_data(proc_list2[0], False)

#if __name__ == '__main__':
#    unittest.main() # runs all unit tests