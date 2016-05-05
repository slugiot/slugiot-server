#########################################################################
## Define API for interacting with procedure table
## These methods will be used in the controller, called by the code
## that actually performs the sync to interact with the tables
##
## Additionally, these methods will be used by the editor team to
## perform saves and stable saves
#########################################################################

import proc_harness_module as phm
import json

proc_table = db.procedures
revisions_table = db.procedure_revisions

####### API FOR PROCEDURE HARNESS TEAM ##########

def get_procedure_status():
    """
    Called upon client request for procedure info

    :param device_id: Device id for which the procedure sync is being performed
    :type device_id: long
    :return Dict of the format {procedure_id: last_update_stable}
                    that specifies the last save time for each procedure associated with the device
    :rtype:
    """
    device_id = request.args(0) if request.args else None

    # Get all procedure_ids for the device_id
    procedure_rows = db(proc_table.device_id == device_id).select(proc_table.id)

    # Build dictionary containing last_update date for each procedure_id
    procedure_info = {}
    for row in procedure_rows:
        pid = row.id
        procedure_info[pid] = db(revisions_table.procedure_id == pid).select(revisions_table.last_update).first().last_update

    return response.json(procedure_info)


def get_procedure_data():
    """
    Called in response to client request for procedures to be synced

    :param procedure_id_lst: List of procedure IDs that need to be updated on client
    :type procedure_id_lst:
    :return: Dict of the format {procedure_id: procedure_data}
    :rtype:
    """

    procedure_id_lst = json.loads(request.vars.items()[0][0])

    # Build dictionary containing data for each procedure_id
    procedures_for_update = {}
    for proc in procedure_id_lst:
        procedures_for_update[proc] = phm.get_procedure_data(proc, True)

    return response.json(procedures_for_update)


def get_procedure_names():
    """
    Called in response to client request for procedures to be synced

    :param procedure_id_lst: List of procedure IDs that need to be updated on client
    :type procedure_id_lst:
    :return: Dict of the format {procedure_id: procedure_data}
    :rtype:
    """
    procedure_id_lst = json.loads(request.vars.items()[0][0])

    # Build dictionary containing data for each procedure_id
    procedures_for_update = {}
    for proc in procedure_id_lst:
        procedures_for_update[proc] = phm.get_procedure_name(proc)

    return response.json(procedures_for_update)