from gluon import current
from perm_comparator import permission_entail


# Permission types.
# v = view
# a = admin (valid only for one whole device)
# e = edit settings of procedure

########################################
##########Manage Permissions############
########################################


def add_permission(device_id, user_email, perm_type='v', procedure_id=None):
    """
    This function add one permission regarding a device to user
    @param device_id : device id
    @param user_email : user email
    @param procedure_id : procedure id if None add generic permission
    @param perm_type : permission type to share
    @returns : if fail return this user's email else return None
    """
    # Check input type value is valid or not
    if perm_type not in ['v', 'e', 'a']:
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
                p.update(perm_user_email=user_email, device_id=device_id, procedure_id=procedure_id,
                         perm_type=perm_type)
    return fail_email


def delete_permission(user_email=None, device_id=None, procedure_id=None):
    """
    This function delete one permission record from user_permission table
    if user_email is None delete all user for specific device_id and procedure.
    if procedure_id is None delete all procedure for specific user and device.
    device_id can't be None.
    @param user_email : user's email
    @param device_id : device id
    @param procedure_id : procedure id
    @returns : Success or not
    """
    db = current.db
    # if user_email is None then delete permissions for all permissions regarding that device_id and procedure_id
    if user_email is None:
        if device_id is None:
            raise Exception("missing device_id")
        # if procedure_id is None delete all procedure regarding this device_id
        if procedure_id is None:
            db(db.user_permission.device_id == device_id).delete()
        else:
            db((db.user_permission.device_id == device_id) &
               (db.user_permission.procedure_id == procedure_id)).delete()
    else:
        if device_id is None:
            raise Exception("missing device_id")
        # if procedure_id is None then delete all permissions regarding to the device
        if procedure_id is None:
            db((db.user_permission.perm_user_email == user_email) &
               (db.user_permission.device_id == device_id)).delete()
        else:
            db((db.user_permission.perm_user_email == user_email) &
               (db.user_permission.device_id == device_id) &
               (db.user_permission.procedure_id == procedure_id)).delete()


####################################################
##########Generate device list for User#############
####################################################


def generate_device_list(user_email):
    """
    This function generate all related devices for a user
    @param user_email: user email
    @return: list of devices
    """
    db = current.db
    p = db((db.user_permission.perm_user_email == user_email))
    return [record.device_id for record in p]


#############################################
##########Access Control methods#############
#############################################


def can_view_procedure(user_email, device_id, procedure_id=None):
    """
    This function check whether a user can view a procedure
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    return check_generic_permission(user_email=user_email, device_id=device_id, perm_type='v') \
           or check_specific_permission(user_email=user_email, device_id=device_id, perm_type='v',
                                        procedure_id=procedure_id)


def can_edit_procedure(user_email, device_id, procedure_id=None):
    """
    This function check whether a user can edit a procedure
    @param device_id : device id
    @param user_email : a list of user email to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    return check_generic_permission(user_email=user_email, device_id=device_id, perm_type='e') \
           or check_specific_permission(user_email=user_email, device_id=device_id, perm_type='e',
                                        procedure_id=procedure_id)


def can_share_procedure(user_email, device_id, procedure_id):
    """
    This function check whether a user can share a procedure, it need 'a' permission type
    @param device_id : device id
    @param user_email : the user who want to share
    @param procedure_id : procedure id
    @returns : whether this user has the permission.
    """
    return check_generic_permission(user_email=user_email, device_id=device_id, perm_type='a') \
           or check_specific_permission(user_email=user_email, device_id=device_id, perm_type='a',
                                        procedure_id=procedure_id)


def can_create_procedure(device_id, user_email):
    """
    This function check whether a user can create a procedure, it need generic 'a' permission type.
    @param device_id : device id
    @param user_email : the user who want to create procedure
    @returns : whether this user has the permission.
    """
    return check_generic_permission(user_email=user_email, device_id=device_id, perm_type='a')


def can_delete_procedure(device_id, user_email, procedure_id=None):
    """
        This function check whether a user can delete a procedure, it need 'a' permission type
        @param device_id : device id
        @param user_email : the user who want to create procedure
        @param procedure_id : the procedure to be deleted, if None ask for generic permission
        @returns : whether this user has the permission.
        """

    return check_generic_permission(user_email=user_email, device_id=device_id, perm_type='a') \
           or check_specific_permission(user_email=user_email, device_id=device_id, perm_type='a',
                                        procedure_id=procedure_id)


def check_generic_permission(device_id, user_email, perm_type):
    db = current.db
    # Does the user have generic permission to the whole device?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == None)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, perm_type)
    return False


def check_specific_permission(device_id, user_email, perm_type, procedure_id):
    db = current.db
    # Does the user have specific permission to this procedure?
    p = db((db.user_permission.perm_user_email == user_email) &
           (db.user_permission.device_id == device_id) &
           (db.user_permission.procedure_id == procedure_id)).select().first()
    if p is not None:
        return permission_entail(p.perm_type, perm_type)
    # No permission, sorry.
    return False
