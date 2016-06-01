import proc_harness_module
import time


def modalprocedure():
    # Device ID should not be changeable
    db.procedures.device_id.writable = False
    val = request.vars['device']
    try:
        db.procedures.device_id.default = val
    except:
        session.flash = T('No such device')

    form3 = SQLFORM(db.procedures)

    # set the logger logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # initialize name variable
    name = ""

    # Generate a name to be passed on to add_permission
    if db(db.device.device_id == val).select():
        name = db(db.device.device_id == val).select()[0].name + "_procedure"

    if form3.process().accepted:
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
    return dict(form3=form3)
