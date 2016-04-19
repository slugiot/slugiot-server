#########################################################################
## This file defines access control methods, including verification, setting and deleting.
## - access_view can view only.
## - access_setting can change settings, and view variables/output, but cannot change procedure code.
## - access_manage can do everything the main user can do.
#########################################################################


#########################################################################
# Verification methods
#########################################################################

# return if the user has authority to view device
def access_view(user_id, device_token):
    return auth.has_permission(name="view", group_id=(device_token + "_" + user_id), user_id=user_id)


# return if the user has authority to configure device
def access_setting(user_id, device_token):
    return auth.has_permission(name="setting", group_id=(device_token + "_" + user_id), user_id=user_id)


# return if the user has authority to share the device with others
def access_manage(user_id, share_user_email, device_token):
    return auth.has_permission(name="manage", group_id=(device_token + "_" + user_id), user_id=user_id)


#########################################################################
# Setting methods
#########################################################################

# give user_id "view" access to "device_token"
def set_access_view(user_id, device_token):
    return auth.add_permission(name="view", group_id=(device_token + "_" + user_id), user_id=user_id)


# give user_id "setting" access to "device_token"
def set_access_setting(user_id, device_token):
    return auth.add_permission(name="setting", group_id=(device_token + "_" + user_id), user_id=user_id)


# give user_id "manage" access to "device_token"
def set_access_manage(user_id, device_token):
    return auth.add_permission(name="manage", group_id=(device_token + "_" + user_id), user_id=user_id)


#########################################################################
# deleting methods
#########################################################################

#delete user_id "view" access to "device_token"
def del_access_view(user_id, device_token):
    return auth.del_permission(name="view", group_id=(device_token + "_" + user_id))

#delete user_id "setting" access to "device_token"
def del_access_setting(user_id, device_token):
    return auth.del_permission(name="setting", group_id=(device_token + "_" + user_id), user_id=user_id)

#delete user_id "manage" access to "device_token"
def del_access_manage(user_id, device_token):
    return auth.del_permission(name="manage", group_id=(device_token + "_" + user_id), user_id=user_id)
