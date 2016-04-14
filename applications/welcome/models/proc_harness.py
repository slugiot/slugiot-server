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

def save(procedure_entry): #not exactly sure what this method needs
    pass

def save_stable(procedure_entry): #will be defined the same way as save expect for specific timestamp updated
    pass

# will be used to create dictionary of procedure statuses
def get_last_update_stable(procedure_id):
    return db.proc_table(last_update_stable, procedure_id==procedure_id)

# not sure if we need this on the server but probably a good idea just to have it
def cleanup_procedure_table(procedure_id):
    pass