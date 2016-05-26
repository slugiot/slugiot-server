import access


def modaladd():
    """
    Description: Controller for the add page, which lets you add a device into the DB
    Returns: A form that lets you add things into db.devices (use by including {{=form}})
    """
    db.device.device_id.writable = False
    db.device.device_id.readable = False # We don't want to display it here.
    db.device.user_email.readable = False # We know who we are.
    form2 = SQLFORM(db.device)
    form2.custom.widget.name['requires'] = IS_NOT_EMPTY()
    if form2.process().accepted:
        device_id = form2.vars.device_id
        access.add_permission(user_email=auth.user.email, perm_type='a', device_id=device_id)
        session.flash = "Device added!"
        redirect(URL('default', 'new_device', args=[form2.vars.id], user_signature=True))
    return dict(form2=form2)
