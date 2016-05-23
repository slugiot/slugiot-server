import access

@auth.requires_login()
def edit():
    """"This allows us to edit permissions for a device.  We imagine we deal only
    with the view permission here."""
    device_id = request.args(0)
    procedure_id = request.args(1)
    # validate them: user has to be manager.
    if not access.can_share_procedure(auth.user.email, device_id, procedure_id)
        raise HTTP(403)
    # Gets list of users who can view.
    user_list = db(etc etc).select()
    user_emails = [u.email for u in user_list]
    # Let's get a nice form for editing this.
    form = SQLFORM.factory(
        Field('users', 'list:string', default=user_emails),
    )
    if form.process().accepted:
        new_users = set(form.vars.users)
        old_users = set(user_emails)
        # Delete old permissions of users who can no longer access.
        for u in old_users - new_users:
            db(db.permissions.procedure == procedure_id && db.permissions.user == u ...).delete()
        # Add permissions of users who can newly access.
        for u in new_users - old_users:
            db.permissions.insert(....)
    return dict(form=form)

"""
{extend 'layout.html'}

{{=form}}


"""