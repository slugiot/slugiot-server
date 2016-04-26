import datetime
import access
from gluon import current

db = current.db
proc_table = db.procedures
revisions_table = db.procedure_revisions

####### API FOR EDITOR TEAM ##########

def create_procedure(procedure_name, user_email, device_id):
    """
    This function should be called when a new procedure is created in the editor.

    :param procedure_name: Name of the new procedure
    :type procedure_name: str
    :param user_email: User email associated with the account that created the procedure
    :type user_email: str
    :return: ID associated with new procedure (procedure_id in revisions table)
    :rtype: long
    """

    if not access.can_create_procedure(device_id, user_email):
        return None

    pid = proc_table.insert(user_email = user_email, device_id = device_id, name = procedure_name)

    # not sure if we really need all these tables
    db.runs_on.insert(device_id = device_id, procedure_id = pid, procedure_name = procedure_name)
    access.add_permission(device_id = device_id, user_email = user_email, procedure_id = pid)
    return pid

def get_procedures_for_user_edit(user_email, device_id):
    """
    This function returns all procedure IDs that are associated with a given user to edit

    :param user_email: User email associated with the account that is trying to access their procedures
    :type user_email: str
    :return: List of procedure IDs associated with user_email
    :rtype:
    """

    # Get all relevant records for user_email
    records = db((proc_table.user_email == user_email) &
                 (proc_table.device_id == device_id)).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        if access.can_edit_procedure(user_email, device_id, row.id):
            procedure_ids.append(row.id)

    return procedure_ids

def get_procedures_for_user_view(user_email, device_id):
    """
    This function returns all procedure IDs that are associated with a given user to view ONLY

    :param user_email: User email associated with the account that is trying to access their procedures
    :type user_email: str
    :return: List of procedure IDs associated with user_email
    :rtype:
    """

    # Get all relevant records for user_email
    records = db((proc_table.user_email == user_email) &
                 (proc_table.device_id == device_id)).select()

    # Create list of procedure IDs from records
    procedure_ids = []
    for row in records:
        if (not access.can_edit_procedure(user_email, device_id, row.id)) and\
                access.can_view_procedure(user_email, device_id, row.id):
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