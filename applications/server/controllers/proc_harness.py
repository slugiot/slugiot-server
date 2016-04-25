#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
##
## Additionally, these methods will be used by the editor team to
## perform saves and stable saves
#########################################################################

import datetime

proc_table = db.procedures
revisions_table = db.procedure_revisions


####### API FOR PROCEDURE HARNESS TEAM ##########


def get_procedure_status(device_id):
    """
    Called upon client request for procedure info

    :param device_id: Device id for which the procedure sync is being performed
    :type device_id: long
    :return Dict of the format {procedure_id: last_update_stable}
                    that specifies the last save time for each procedure associated with the device
    :rtype:
    """

    # Get all procedure_ids for the device_id
    procedure_ids = db((devices.device_id == device_id) &
                       (devices.user_id == proc_table.user_id)).select(proc_table.procedure_id)

    # Build dictionary containing last_update date for each procedure_id
    procedure_info = {}
    for proc in procedure_ids:
        pid = proc.procedure_id
        procedure_info[pid] = db(revisions_table.procedure_id == pid).select(revisions_table.last_update).first().last_update

    return procedure_info


def get_procedure_update(procedure_id_lst):
    """
    Called in response to client request for procedures to be synced

    :param procedure_id_lst: List of procedure IDs that need to be updated on client
    :type procedure_id_lst:
    :return: Dict of the format {procedure_id: procedure_data}
    :rtype:
    """
    # Build dictionary containing data for each procedure_id
    procedures_for_update = {}
    for proc in procedure_id_lst:
        procedures_for_update[proc.procedure_id] = get_procedure_data(proc, True)

    return procedures_for_update