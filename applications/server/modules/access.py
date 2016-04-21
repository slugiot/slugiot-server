from gluon import current
from gluon import auth
from perm_comparator import permission_max
from perm_comparator import permission_min
from perm_comparator import permission_entail


# Permission types.
# v = view
# a = admin (valid only for one whole device)
# e = edit settings of procedure

def register_device(name=None, description=''):
    """
    This function register a device into device_table
    @param name : device name
    @param description : device description
    """
    db = current.db
    devices = db.devices
    permission = db.user_permission
    device_id = devices.insert(name=name, user_id=auth.user_id, description=description)
    permission.insert(perm_user_email=auth.user.email, device_id=device_id, procedure_id=None, perm_type='a')


# TODO: perhaps useful to the UI team.


def share_device(device_id, user_email=[], _type='v', procedure_id=None):
    """
    This function share one device to multiple users with one permission type return
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @param _type : permission type to share
    @returns : the user email list that do not register
    """
    db = current.db
    permission = db.user_permission
    fail_email = []
    for email in user_email:
        # Does the email exist in registered user table?
        # if it does not exist this permission adding operation is denied
        if db(db.auth_user.email == email) is None:
            fail_email.append(email)
        else:
            # Does permission table contain this record?
            p = db((db.user_permission.perm_user_email == email) &
                   (db.user_permission.device_id == device_id) &
                   (db.user_permission.procedure_id == procedure_id)).select().first()

            if p is None:
                # if no record stored in permission table we insert new permission record
                permission.insert(perm_user_email=email, device_id=device_id, procedure_id=procedure_id,
                                  perm_type=_type)
            else:
                # update the selected row if given type entails original type
                if permission_entail(_type, p.perm_type):
                    p.update(perm_user_email=email, device_id=device_id, procedure_id=procedure_id, perm_type=_type)
    return fail_email


def can_view_procedure(user_email, device_id, procedure_id):
    """
    This function check whether a user can view a procedure
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()

    if p is not None:
        return permission_entail(p.perm_type, 'v')

    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, 'v')

    # No permission, sorry.
    return False


def can_edit_procedure(user_email, device_id, procedure_id):
    """
    This function check whether a user can edit a procedure
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, 'e')

    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, 'e')

    # No permission, sorry.
    return False


def can_share_procedure(user_email, device_id, procedure_id):
    """
    This function check whether a user can share a procedure, it need 'a' permission type
    @param device_id : device id
    @param user_email : the user who want to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, 'a')

    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, 'a')

    # No permission, sorry.
    return False


def can_create_procedure(device_id, user_email):
    """
    This function check whether a user can create a procedure, it need 'a' permission type
    @param device_id : device id
    @param user_email : the user who want to create procedure
    @returns : whether this user has the permission.
    """

    db = current.db

    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id is None)).select().first()
    # it need admin permission
    if p.perm_type is 'a':
        return True
    return False
