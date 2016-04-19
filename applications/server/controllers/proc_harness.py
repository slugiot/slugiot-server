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

####### API FOR EDITOR TEAM ##########

def create_procedure(procedure_name, user_email, device_id):
    """
    This function should be called when a new procedure is created in the editor.

    :param procedure_name: Name of the new procedure
    :type procedure_name: str
    :param user_id: User id associated with the account that created the procedure
    :type user_id: str
    :return: ID associated with new procedure (procedure_id in revisions table)
    :rtype: long
    """
    return proc_table.insert(user_email = user_email, device_id = device_id, name = procedure_name)


def get_procedures_for_user(user_id, device_id):
    """
    This function returns all procedure IDs that are associated with a given user

    :param user_id: User id associated with the account that is trying to access their procedures
    :type user_id: str
    :return: List of procedure IDs associated with user_id
    :rtype:
    """

    # Get all relevant records for user_id
    records = db((proc_table.user_id == user_id) &
                 (proc_table.device_id == device_id)).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        procedure_ids.append(row.id)

    return procedure_ids


# Do we have to worry about stuff coming in at the same time? Currently a bug
def get_procedure_data(procedure_id, stable):
    """
    Returns actual code that corresponds to a given procedure ID.
    Returns either the most recent stable version or the most recent absolute version.

    :param procedure_id: Procedure ID for which code should be fetched
    :type procedure_id: long
    :param stable: Flag that determines whether the code returned should be most recent stable or just the most recent
    :type stable: bool
    :return: Data stored for the procedure
    :rtype: str
    """

    # Get the most recent date, either stable or absolute
    max = revisions_table.last_update.max()
    if stable:
        date = db((revisions_table.procedure_id == procedure_id) &
                  (revisions_table.stable_version == stable)).select(max).first()[max]
    else:
        date = db(revisions_table.procedure_id == procedure_id).select(max).first()[max]

    # Return the data corresponding the procedure ID and determined date
    return db((revisions_table.procedure_id == procedure_id) &
              (revisions_table.last_update == date)).select(revisions_table.procedure_data).first().procedure_data


def save(procedure_id, procedure_data, stable):
    """
    Save code corresponding to a procedure ID as either a stable version or a temporary version

    :param procedure_id: Procedure ID for which code should be fetched
    :type procedure_id: long
    :param procedure_data: Code that should be saved
    :type procedure_data: str
    :param stable: Flag that determines whether the code should be sent to client on next request or not
    :type stable: bool
    """

    # Insert new record to revisions table
    revisions_table.insert(procedure_id = procedure_id,
                           procedure_data = procedure_data,
                           last_update = datetime.datetime.utcnow(),
                           stable_version = stable)

    # Only keep temporary revisions until next stable revision comes in
    # Clean up old temporary revisions upon stable save
    if stable:
        db((revisions_table.procedure_id == procedure_id) &
           (revisions_table.stable_version == False)).delete()


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