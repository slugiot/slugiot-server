####################### TEST CODE #######################

from gluon.custom_import import track_changes; track_changes(True)

import proc_harness_module as phm
import random
#import os
import access
import time
from gluon import current
from gluon.tools import Auth
import logging

test_device_id = "test"
logger = logging.getLogger("web2py.app.server")
logger.setLevel(logging.INFO)

auth = Auth(globals(), current.db)

#@auth.requires_login()
def index():
    test = ProcHarnessTest()
    test.run_editor_api_test()
    return "Ran Unit Tests for Procedure Harness"

def clear_tables():
    if request.env.HTTP_HOST.find('localhost') == -1 and request.env.HTTP_HOST.find('127.0.0.1') == -1:
        raise(HTTP(403))
    db = current.db
    db.procedures.truncate()
    db.procedure_revisions.truncate()
    if db(db.procedures).isempty() and db(db.procedure_revisions).isempty():
        logger.info("Server Table Cleared")

def create_new_proc_for_synch():
    if request.env.HTTP_HOST.find('localhost') == -1 and request.env.HTTP_HOST.find('127.0.0.1') == -1:
        raise(HTTP(403))
    random.seed(time.time())
    name = "new_procedure" + str(random.randint(0,10000))

    db = current.db
    auth = current.auth
    test_user_email = auth.user.email
    logger.info("test_user_email" + str(test_user_email))

    access.add_permission(test_device_id, test_user_email, perm_type="a")
    logger.info("added perm")

    proc_id = phm.create_procedure(name, test_device_id)
    logger.info("created proc")

    phm.save(proc_id, "SOME DATA!", True)
    logger.info("look for proc_id and name: " + str(proc_id) + " " + str(name))


def update_proc_for_synch():
    if request.env.HTTP_HOST.find('localhost') == -1 and request.env.HTTP_HOST.find('127.0.0.1') == -1:
        raise(HTTP(403))
    db = current.db
    proc_table = db.procedures

    proc_id = db(proc_table.id).select().first().id
    proc_name = db(proc_table.id == proc_id).select().first().name
    random.seed(time.time())
    new_data = "new_data" + str(random.randint(0,10000))

    phm.save(proc_id, new_data, True)
    logger.info("look for proc_id, name, data : " + str(proc_id) + " " + str(proc_name) + " " + str(new_data))


def update_proc_not_for_synch():
    if request.env.HTTP_HOST.find('localhost') == -1 and request.env.HTTP_HOST.find('127.0.0.1') == -1:
        raise(HTTP(403))
    db = current.db
    proc_table = db.procedures

    proc_id = db(proc_table.id).select().first().id
    proc_name = db(proc_table.id == proc_id).select().first().name
    random.seed(time.time())
    new_data = "new_data" + str(random.randint(0,10000))
    phm.save(proc_id, new_data, False)
    logger.info("should not see data : " + str(new_data) + " for id, name " + str(proc_id) + " " + str(proc_name))

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
        auth = Auth(globals(), self.db)
        self.test_user_email = "test@test.com" #auth.user.email
        access.add_permission(self.test_device_id, self.test_user_email, perm_type="a")

        self.proc_table = self.db.procedures
        self.revisions_table = self.db.procedure_revisions

    def run_editor_api_test(self):

        self.proc_table.truncate()
        self.revisions_table.truncate()

        name = "test_name"
        proc_id = phm.create_procedure(name, self.test_device_id)

        for row in self.db(self.proc_table).select():
            logging.debug(str(row))

        test_data = "#let's do a test with a newline\n how much text do we have?"
        phm.save(proc_id, test_data, True)
        time.sleep(2)
        test_data2 = "this is a stupid edit"
        phm.save(proc_id, test_data2, False)
        time.sleep(2)

        for row in self.db(self.revisions_table).select():
            logger.debug(str(row))

        name2 = "illegal test name"
        proc_id2 = phm.create_procedure(name2, self.test_device_id)
        test_data3 = "db = 2\nprint db"

        phm.save(proc_id2, test_data3, True)
        time.sleep(2)
        test_data4 = "this is another stupid edit"
        phm.save(proc_id2, test_data4, False)

        # get the list of procedure_id from device
        proc_list1 = phm.get_procedures_for_edit(self.test_device_id)
        proc_list2 = phm.get_procedures_for_view(self.test_device_id)

        logger.debug("proc list 1 " + str(proc_list1))
        logger.debug("proc list 2 " + str(proc_list2))

        # get the data of procedure
        data1 = phm.get_procedure_data(proc_list1[0], True)

        logger.debug(data1) #should be test_data_1
        logger.debug("Editor test complete")
