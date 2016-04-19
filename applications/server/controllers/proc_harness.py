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
