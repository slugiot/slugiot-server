import proc_harness_module
import access
import time


def modalprocedure():
    # Device ID should not be changeable
    val = request.vars['device_id']
    print "TEST123 " + val
    try:
        print "TEST123 VALUE: " + val
        db.procedures.device_id.default = val
    except:
        print "TEST123 THIS DIDN'T WORK POTATO"
        session.flash = T('No such device')

    # TODO: Make it so the form itself doesn't add anything into the database
    form3 = SQLFORM(db.procedures)

    # set the logger logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # initialize name variable
    name = ""

    # Generate a name to be passed on to add_permission
    # Only works with device ID specified in URL, try in editor
    if db(db.device.device_id == val).select():
        name = db(db.device.device_id == val).select()[0].name + "_procedurelololol"
        print "TEST VALUE NAME : " + name

    if auth.is_logged_in() is False:
        placeholder_email = 'blah@blah.com'
    else:
        placeholder_email = auth.user.email

    access.add_permission("abaae86a-f073-460c-8641-f75328d81b87", placeholder_email, perm_type="a")

    if form3.process().accepted:
        # create procedure name=demo_1 for the device whose id = 1 and saved it
        proc_id = proc_harness_module.create_procedure(name, "abaae86a-f073-460c-8641-f75328d81b87")
        print proc_id
        proc_harness_module.save(proc_id,
                                 "#demo1 stable edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered",
                                 True)
        time.sleep(2)
        proc_harness_module.save(proc_id,
                                 "#demo1 temporary edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered",
                                 False)
        time.sleep(2)
        # Go back to the home page.
        session.flash = "Procedure added!"
    return dict(form3=form3)
