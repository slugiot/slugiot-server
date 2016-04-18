from gluon import current
from gluon import auth


# Permission types.
# v = view
# a = admin (valid only for one whole device)
# e = edit settings of procedure

def register_device(name=None, description=''):
    db = current.db
    devices = db.devices
    permission = db.user_permission
    device_id = devices.insert(name=name, user_id=auth.user_id, description=description)
    permission.insert(perm_user_email=auth.user.email, device_id=device_id, procedure_id=None, perm_type='a')


# Share one device to multiple users with one permission type
# return emails which are not successfully shared.
def share_device(device_id, user_email={}, type='v', procedure_id=None):
    db = current.db
    permission = db.user_permission
    fail_email = {}
    for email in user_email:
        # Does the email exist in registered user table?
        # if it does not exist this permission adding operation is denied
        if db(db.auth_user.email == email) is None:
            fail_email += email
        else:
            p = db((db.user_permission.perm_user_email == email) &
                   (db.user_permission.device_id == device_id) &
                   (db.user_permission.procedure_id == procedure_id)).select().first()

            if p is None:
                # if no record stored in permission table we insert new permission record
                permission.insert(device_id=device_id, user_email=email, procedure_id=procedure_id, perm_type=type)
            else:
                p.update(device_id=device_id, user_email=email, procedure_id=procedure_id, perm_type=type)
    return fail_email


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


def can_edit_procedure(user_email, device_id, procedure_id):
    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()
    if p.perm_type in {'e', 'a'}:
        return True

    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p.perm_type in {'e'}:
        return True

    # No permission, sorry.
    return False
