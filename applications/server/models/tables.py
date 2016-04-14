#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

from datetime import datetime

# TODO: Restrict r/w permissions?
# we would perhaps need another DB for logs and massive amounts of text like that?
# is another team taking care of those?

# This is a table for what rasberry pi devices a user owns
db.define_table('rbp_devices',
                # we can always an ID for something
                Field('user_id', db.auth_user, default=auth.user_id),
                # user should give rbp a name
                Field('name', 'string', required=True, default='Unknown Device'),
                # perhaps a description as well?
                Field('description', 'text', default=''),
                # part of what the UI calls for
                Field('last_sync', 'datetime', required=True,default=datetime.utcnow()),
                # status of the device, 0 = OK, 1 = Check Logs, 2 = Malfunction, 3 = Unknown/Unconfigured
                Field('status', 'integer', required=True, default=3),
                # if we give the rbp an ID, we can do checks to verify devices belong to which rbp
                Field('device_id', 'string', required=True)
                )

# sub devices are indv devices connected to each rbp
db.define_table('sub_devices',
                # must match rbp_devices' device_id
                db.Field('rbp_id', 'string', required=True),
                # self explanatory
                db.Field('name', 'text', required=False, default=''),
                # status of the device, 0 = OK, 1 = Check Logs, 2 = Malfunction, 3 = Unknown/Unconfigured
                Field('status', 'integer', required=True, default=3),
                # when was the device last active/synced?
                db.Field('is_active', 'boolean', required=False, default=True),
                # who added the device and when?
                db.Field('added_on', 'datetime', required=True),
                db.Field('added_by', db.auth_user, default=auth.user_id))
