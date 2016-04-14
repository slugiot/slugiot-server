
#return if the user has authority to view device
def access_view(user_id, device_token):
    return auth.has_permission(name="view",group_id=device_token,user_id=user_id)
#return if the user has authority to configure device
def access_setting(user_id, device_token):
    return auth.has_permission(name="setting", group_id=device_token, user_id=user_id)
#return if the user has authority to share the device with others
def access_manage(user_id, share_user_email, device_token):
    return auth.has_permission(name="manage", group_id=device_token, user_id=user_id)
#set authority relation between user and device
def access_set_authority(user_id, device_token, auth_level, role):
    return auth.add_permission(name=role, group_id=(device_token+auth_level), user_id=user_id)