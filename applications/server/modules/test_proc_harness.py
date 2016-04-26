import proc_harness_module as phm
from gluon import current

db = current.db
proc_table = db.procedures
revisions_table = db.procedure_revisions


def run_test():
    db(proc_table).delete()
    db(revisions_table).delete()
    proc_id = phm.create_procedure("blah", "blah@blah")
    phm.save(proc_id, "blahblah", True)

    proc_id2 = phm.create_procedure("blah2", "blah2@blah")
    phm.save(proc_id2, "blahblah2", False)

    phm.save(proc_id2, "blahblah3", False)

    #for row in db(proc_table).select():
    #    print row.id, row.user_id, row.name
    #for row in db(revisions_table).select():
    #    print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

    proc_list1 = phm.get_procedures_for_user("blah@blah")
    proc_list2 = phm.get_procedures_for_user("blah2@blah")

    for row in db(revisions_table).select():
        print row.procedure_id, row.procedure_data, row.last_update, row.stable_version

    print "first", phm.get_procedure_data(proc_list1[0], True)
    print "second", phm.get_procedure_data(proc_list2[0], False)