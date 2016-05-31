import access


@auth.requires_login()
def edit_view():
    """"This allows us to edit permissions for a device.  We imagine we deal only
    with the view permission here."""
    device_id = request.vars['device_id']
    procedure_id = request.vars['procedure_id']
    # validate them: user has to be manager.
    if not access.can_share_procedure(auth.user.email, device_id, procedure_id):
        raise HTTP(403)
    # Gets list of users who can view.
    user_list = db((db.user_permission.device_id == device_id)&(db.user_permission.procedure_id == procedure_id)).select()
    user_emails = [u.perm_user_email for u in filter(lambda x: x.perm_type=='v', user_list)]
    # Let's get a nice form for editing this.
    form = SQLFORM.factory(
        Field('users', 'list:string', requires=IS_LIST_OF(IS_EMAIL(error_message='must be email!') and IS_IN_DB(db, db.auth_user.email,'%(email)s')), default=user_emails)
    )
    if form.process().accepted:
        new_users = set(form.vars.users) if type(form.vars.users) == type([]) else set([form.vars.users])
        old_users = set(user_emails)
        # Delete old permissions of users who can no longer access.
        for u in old_users - new_users:
            if u != '':
                access.delete_permission(device_id=device_id,user_email=u,procedure_id=procedure_id)
        # Add permissions of users who can newly access.
        for u in new_users - old_users:
            if u != '':
                access.add_permission(device_id,u,'v',procedure_id=procedure_id)
        redirect(URL('edit_permission', 'edit_view', vars={'device_id' : device_id, 'procedure_id': procedure_id}))
    return dict(form=form)

@auth.requires_login()
def edit_edit():
    """"This allows us to edit permissions for a device.  We imagine we deal only
    with the view permission here."""
    device_id = request.vars['device_id']
    procedure_id = request.vars['procedure_id']
    # validate them: user has to be manager.
    if not access.can_share_procedure(auth.user.email, device_id, procedure_id):
        raise HTTP(403)
    # Gets list of users who can view.
    user_list = db((db.user_permission.device_id == device_id)&(db.user_permission.procedure_id == procedure_id)).select()
    user_emails = [u.perm_user_email for u in filter(lambda x: x.perm_type=='e', user_list)]
    # Let's get a nice form for editing this.
    form = SQLFORM.factory(
        Field('users', 'list:string', requires=IS_LIST_OF(IS_EMAIL(error_message='must be email!')), default=user_emails)
    )
    if form.process().accepted:
        new_users = set(form.vars.users) if type(form.vars.users) == type([]) else set([form.vars.users])
        old_users = set(user_emails)
        # Delete old permissions of users who can no longer access.
        for u in old_users - new_users:
            if u != '':
                access.delete_permission(device_id=device_id,user_email=u,procedure_id=procedure_id)
        # Add permissions of users who can newly access.
        for u in new_users - old_users:
            if u != '':
                access.add_permission(device_id,u,'e',procedure_id=procedure_id)
        redirect(URL('edit_permission', 'edit_edit', vars={'device_id' : device_id, 'procedure_id': procedure_id}))
    return dict(form=form)


@auth.requires_login()
def edit_admin():
    """"This allows us to edit permissions for a device.  We imagine we deal only
    with the view permission here."""
    device_id = request.vars['device_id']
    procedure_id = request.vars['procedure_id']
    # validate them: user has to be manager.
    if not access.can_share_procedure(auth.user.email, device_id, procedure_id):
        raise HTTP(403)
    # Gets list of users who can view.
    user_list = db((db.user_permission.device_id == device_id)&(db.user_permission.procedure_id == procedure_id)).select()
    user_emails = [u.perm_user_email for u in filter(lambda x: x.perm_type=='a', user_list)]
    # Let's get a nice form for editing this.
    form = SQLFORM.factory(
        Field('users', 'list:string', requires=IS_LIST_OF(IS_EMAIL(error_message='must be email!')), default=user_emails)
    )
    if form.process().accepted:
        new_users = set(form.vars.users) if type(form.vars.users) == type([]) else set([form.vars.users])
        old_users = set(user_emails)
        # Delete old permissions of users who can no longer access.
        for u in old_users - new_users:
            if u != '':
                access.delete_permission(device_id=device_id,user_email=u,procedure_id=procedure_id)
        # Add permissions of users who can newly access.
        for u in new_users - old_users:
            if u != '':
                access.add_permission(device_id,u,'a',procedure_id=procedure_id)
        redirect(URL('edit_permission', 'edit_admin', vars={'device_id' : device_id, 'procedure_id': procedure_id}))
    return dict(form=form)