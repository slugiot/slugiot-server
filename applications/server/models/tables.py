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

#########################
# Server organization tables.

# Keeps track of devices.
db.define_table('device',
                # if we give the device an ID, we can do checks to verify devices belong to which device
                Field('device_id', 'string', required=True),
                Field('user_email', 'string', default=db.auth_user.email),
                Field('name', 'string', required=True, default='Unknown Device'), # Name of device
                Field('description', 'text', default=''),
                Field('device_icon', 'string', required=True, default='fa-globe')  # FA ID needed by UI team
                )

# This is a table that specifies what procedure runs on what device for what user
db.define_table('runs_on',
                Field('device_id', 'string', required=True),
                Field('procedure_id', 'string', required=True),
                Field('procedure_name'), # Name of the procedure on a particular device.
                )

# with this new split table definition it makes sense to just use the automatic id in this table as the procedure_id
db.define_table('procedures',
                # TODO: add device_id or account or something.
                #Field('procedure_id', 'bigint', required=True),  # key
                Field('user_email', 'string', required=True),
                Field('name', 'string')  # Name of procedure
                )

db.define_table('procedure_revisions',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('procedure_data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                Field('last_update', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('stable_version', 'boolean', required=True) # True for stable False for not stable
                )


##############
# Permission table.

# Permission types.
# v = view
# a = admin (valid only for one whole device)
# e = edit settings of procedure
db.define_table('user_permission',
                Field('perm_user_email', required =True),
                # The email of the currently logged in user can be found in auth.user.email
                Field('device_id', required = True),
                Field('procedure_id'), # If this is Null, then permission is for whole device.
                # If None, then the permission is valid for ALL procedures.
                Field('perm_type',required = True) # 'e'=edit, 'v'=view, etc.
                # See above.
                )


#########################
# Settings are synched "down" to the client.

db.define_table('client_setting',
                Field('device_id'),
                Field('procedure_id'), # Can be Null for device-wide settings.
                Field('setting_name'),
                Field('setting_value'), # Encoded in json-plus.
                Field('last_updated', 'datetime', update=datetime.utcnow())
                )


#########################
## These tables are synched "up" from the clients to the server.

db.define_table('logs',
                Field('device_id'),
                Field('procedure_id'),
                Field('log_level', 'integer'), #  int, 0 = most important.
                Field('log_message', 'text'),
                Field('logged_time_stamp', 'datetime'),
                Field('received_time_stamp', 'datetime', default=datetime.utcnow()),

                )

db.define_table('outputs',
                Field('device_id'),
                Field('procedure_id'),
                Field('name'), # Name of variable
                Field('output_value', 'text'), # Json, short please
                Field('tag'),
                Field('output_time_stamp', 'datetime'),
                Field('received_time_stamp', 'datetime', default=datetime.utcnow()),
)

db.define_table('module_values',
                Field('device_id'),
                Field('time_stamp', 'datetime', default=datetime.utcnow()),
                Field('procedure_id'),
                Field('name'),  # Name of variable
                Field('output_value', 'text'),  # Json, short please
                )

db.logs.log_level.requires = IS_INT_IN_RANGE(0, 4)  # limit log type to 5 (INFO, WARNING, DEBUG, ERROR, CRITICAL)
db.logs.time_stamp.writable=False                   # can not manual change log data (time, log_level, log_message)
db.logs.log_level.writable=False
db.logs.log_message.writable=False

## TODO: define the tables that need to be synched "down", for settings, and procedures.



############ Test tables.
## This is the table used to temporary testing editor
## it get procedure by the table id instead of device id
## because Team2 provide API for us to get the data from procedures
## we will delete this table at the final edition.
db.define_table('coding',
            Field('procedures', 'text'),
            Field('times','datetime')
            )
