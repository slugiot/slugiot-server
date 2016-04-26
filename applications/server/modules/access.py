from gluon import current
from gluon.tools import Auth
from perm_comparator import permission_max
from perm_comparator import permission_min
from perm_comparator import permission_entail


# Permission types.
# v = view
# a = admin (valid only for one whole device)
# e = edit settings of procedure


def add_permission(device_id, user_email, perm_type='v', procedure_id=None):
    """
    This function add one permission of a device to user
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @param perm_type : permission type to share
    @returns : if fail return this user's email else return None
    """
    # Check input type value is valid or not
    if perm_type not in ['v','e','a']:
        raise Exception("Invalid permission type input")

    db = current.db
    permission = db.user_permission
    fail_email = None
    # Does the email exist in registered user table?
    # if it does not exist this permission adding operation is denied
    if db(db.auth_user.email == user_email) is None:
        fail_email = user_email
    else:
        # Does permission table contain this record?
        p = db((db.user_permission.perm_user_email == user_email) &
               (db.user_permission.device_id == device_id) &
               (db.user_permission.procedure_id == procedure_id)).select().first()

        if p is None:
            # if no record stored in permission table we insert new permission record
            permission.insert(perm_user_email=user_email, device_id=device_id, procedure_id=procedure_id,
                              perm_type=perm_type)
        else:
            # update the selected row if given type entails original type
            if permission_entail(perm_type, p.perm_type):
                p.update(perm_user_email=user_email, device_id=device_id, procedure_id=procedure_id, perm_type=perm_type)
    return fail_email


def delete_permission(user_email, device_id, procedure_id):
    """
    This function delete one permission record from user_permission table
    @param user_email : user's email
    @param device_id : device id
    @param procedure_id : procedure id
    @returns : Success or not
    """
    db = current.db
    return \
        db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).delete()


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
           (db.user_permission.procedure_id is None)).select().first()
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
           (db.user_permission.procedure_id is None)).select().first()
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
           (db.user_permission.procedure_id is None)).select().first()
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
