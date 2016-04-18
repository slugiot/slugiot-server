#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
##
## Additionally, these methods will be used by the editor team to
## perform saves and stable saves
#########################################################################

from gluon import current

proc_table = current.db["procedures"]


####### API FOR EDITOR TEAM ##########

# return procedure_id
def create_procedure():
    pass

# return list procedure_id
def get_procedures_for_user(user_id):
    pass

# True for stable gets last stable, False gets most recent stable or not
def get_procedure_data(procedure_id, stable):
    pass

# True for stable is save stable, False is save temp
# when save is stable, flush all temp versions
def save(procedure_id, stable):
    pass


####### API FOR PROCEDURE HARNESS TEAM ##########

# called in response to client request for procedure info
# returns a dictionary of the format {procedure_id, last_update_stable}
def get_procedure_status(device_id):
    # 1. Get all procedure_ids for the device_id
    # 2. build dictionary containing last_update_stable date for each procedure_id
    # 3. return dictionary
    #     return db.proc_table(last_update_stable, procedure_id==procedure_id)
    pass

# not sure if we need this on the server but probably a good idea just to have it
def cleanup_procedure_table(procedure_id):
    pass
