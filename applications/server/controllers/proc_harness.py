#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
##
## Additionally, these methods will be used by the editor team to
## perform saves and stable saves
#########################################################################

from gluon import current

db = current.db
proc_table = db.procedures

####### API FOR EDITOR TEAM ##########

# return procedure_id to be used for a new procedure being created
# note - currently this function does NOT implicitly save the procedure_id in the table
def create_procedure():
    if proc_table.isempty():
        proc_id = 1
    current_proc_max = proc_table.procedure_id.max()
    proc_id = current_proc_max + 1
    return proc_id

# return list procedure_id
# alternatively: return db(proc_table.user_id == user_id).select(proc_table.procedure_id)
# second option returns Rows object not list
def get_procedures_for_user(user_id):
    records = db(proc_table.user_id == user_id).select()
    procedure_ids = []
    for row in records:
        procedure_ids.append(row.procedure_id)
    return procedure_ids

# True for stable gets last stable, False gets most recent stable or not
def get_procedure_data(procedure_id, stable):
    if stable:
        date = db(proc_table.procedure_id == procedure_id,
                  proc_table.stable == stable).select(proc_table.last_update).max()
    else:
        date = db(proc_table.procedure_id == procedure_id).select(proc_table.last_update).max()
    return db(proc_table.procedure_id == procedure_id,
              proc_table.last_update == date).select(proc_table.data)

# True for stable is save stable, False is save temp
# when save is stable, flush all temp versions
def save(procedure_id, procedure_data, stable):
    # insert new record
    proc_table.insert(procedure_id = procedure_id,
                      procedure_data = procedure_data,
                      stable = stable)
    #flush temp versions for stable save
    if stable:
        db(proc_table.procedure_id == procedure_id,
           proc_table.stable == False).delete()

####### API FOR PROCEDURE HARNESS TEAM ##########

# called in response to client request for procedure info
# returns a dictionary of the format {procedure_id, last_update_stable}
def get_procedure_status(device_id):
    # 1. Get all procedure_ids for the device_id
    procedure_ids = db(db.devices.device_id == device_id,
                       db.devices.user_id == proc_table.user_id).select(proc_table.procedure_id)
    # 2. build dictionary containing last_update_stable date for each procedure_id
    procedure_info = {}
    for proc in procedure_ids:
        procedure_info[proc] = get_procedure_data(proc, True)
    # 3. return dictionary
    return procedure_info