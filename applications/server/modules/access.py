from gluon import current

def can_view_procedure(user_email, device_id, procedure_id):
    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()
    if p.perm_type in {'v', 'e', 'a'}:
        return True

    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p.perm_type in {'v', 'e'}:
        return True

    # No permission, sorry.
    return False
