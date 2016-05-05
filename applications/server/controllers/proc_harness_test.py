####################### TEST CODE #######################

from gluon.custom_import import track_changes; track_changes(True)

import proc_harness_module as phm
import random
#import os
import access
import time
from gluon import current
from gluon.tools import Auth

def index():
    test = ProcHarnessTest()
    test.run_editor_api_test()
    return "Ran Unit Tests for Procedure Harness"

class ProcHarnessTest:
    def __init__(self):
        #try:
        #    os.remove("applications/server/testdatabases")
        #except:
        #    pass
        #os.system("cp -r applications/server/databases applications/server/testdatabases")

        # This approach won't work for GAE because it isn't using SQLite.
        #self.db = DAL('sqlite://storage.sqlite', folder='applications/server/testdatabases/',
        #          pool_size="10",
        #          migrate_enabled="true",
        #          check_reserved=['all']
        #          )

        self.db = current.db

        # The database will be empty until we populate it with table structure
        #filename = "applications/server/models/tables.py"
        #with open(filename, 'rb+') as tables_code:
        #    exec (tables_code.read())

        #print "tables!!", self.db.tables

        self.test_device_id = "test"
        self.test_user_email = auth.user.email
        access.add_permission(self.test_device_id, self.test_user_email, perm_type="a")

        self.proc_table = self.db.procedures
        self.revisions_table = self.db.procedure_revisions

    def run_editor_api_test(self):

        self.db(self.proc_table).delete()
        self.db(self.revisions_table).delete()

        name = "test_name"
        proc_id = phm.create_procedure(name, self.test_device_id)

        for row in self.db(self.proc_table).select():
            print row

        test_data = "#let's do a test with a newline\n how much text do we have?"
        phm.save(proc_id, test_data, True)
        time.sleep(2)
        test_data2 = "this is a stupid edit"
        phm.save(proc_id, test_data2, False)
        time.sleep(2)

        for row in self.db(self.revisions_table).select():
            print row

        name2 = "second_test_name"
        proc_id2 = phm.create_procedure(name2, self.test_device_id)
        test_data3 = "db = 2\nprint db"

        phm.save(proc_id2, test_data3, True)
        time.sleep(2)
        test_data4 = "this is another stupid edit"
        phm.save(proc_id2, test_data4, False)

        # get the list of procedure_id from device
        proc_list1 = phm.get_procedures_for_edit(self.test_device_id)
        proc_list2 = phm.get_procedures_for_view(self.test_device_id)

        print "proc list 1", proc_list1
        print "proc list 2", proc_list2 # should be empty

        # get the data of procedure
        data1 = phm.get_procedure_data(proc_list1[0], True)

        print data1 #should be test_data_1
        print "Editor test complete"

    def create_new_proc_for_synch(self):
        name = "new_procedure" + str(random.randint())
        proc_id = phm.create_procedure(name, self.test_device_id)
        print "look for proc_id and name: ", proc_id, name

    def update_proc_for_synch(self):
        proc_id = self.db(self.proc_table).select(id).first().id
        new_data = "new_data\n" + str(random.randint())
        phm.save(proc_id, new_data, True)
        print "look for proc_id, data : ", proc_id, new_data

    def update_proc_not_for_synch(self):
        proc_id = self.db(self.proc_table).select(id).first().id
        new_data = "new_data\n" + str(random.randint())
        phm.save(proc_id, new_data, False)
        print "should not see: ", proc_id, new_data