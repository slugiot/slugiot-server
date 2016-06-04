import proc_harness_module
import access
import time


def modalprocedure():
    # Device ID should not be changeable
    val1 = request.vars['device']
    if val1 is None:
        print "val1 is None"
    else:
        print "val1 is: " + val1
    val = None
    if val1 is not None:
        val = db(db.device.id == val1).select()[0].device_id
        print val
    try:
        db.procedures.device_id.default = val
    except:
        session.flash = T('No such device')

    # TODO: Make it so the form itself doesn't add anything into the database
    form3 = SQLFORM(db.procedures_trash) # form3.vars.name

    # set the logger logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # initialize name variable
    name = ""

    # Generate a name to be passed on to add_permission
    # Only works with device ID specified in URL, try in editor

    name1 = request.vars.name
    if name1 is not None:
        name = name1.replace(" ", "")
    else:
        name = name1
    print name

    """
    if db(db.device.device_id == val).select():
        name = db(db.device.device_id == val).select()[0].name + "_procedure"
        #  db(db.device.device_id == val).select()[0].id
    """

    if auth.is_logged_in() is False:
        placeholder_email = 'blah@blah.com'  # to make web2py shut up when you're not logged in
    else:
        placeholder_email = auth.user.email

    access.add_permission(val, placeholder_email, perm_type="a")

    if form3.process().accepted:
        print "Procedure Accepted"
        # create procedure name=demo_1 for the device whose id = 1 and saved it
        proc_id = proc_harness_module.create_procedure(name, val)
        print "Procedure values are: " + name
        proc_harness_module.save(proc_id,
                                 "#demo1 stable edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered",
                                 True)
        time.sleep(1)
        proc_harness_module.save(proc_id,
                                 "#demo1 temporary edition code\nfrom procedureapi import Procedure\n\nclass DeviceProdecure (Procedure):\n\n    def init (self):\n        # initialize variables\n        # Add schedule. For example:\n        # self.api.add_schedule(repeats=10, period_between_runs=86400)\n\n    def run (self):\n        # Called each time the schedule is triggered",
                                 False)
        # Go back to the home page.
        session.flash = "Procedure added!"
        redirect(URL('editor', 'test_edit', vars=dict(device_id=val1, procedure_id = proc_id, stable='true')))
    return dict(form3=form3)
