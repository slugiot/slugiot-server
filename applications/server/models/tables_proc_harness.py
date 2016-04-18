import datetime

## These correspond to client tables.

db.define_table('logs',
                Field('device_id'),
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('level', 'integer'), #  int, 0 = most important.
                Field('message', 'text'),
                )

db.define_table('output',
                Field('device_id'),
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'), # Name of variable
                Field('value', 'text'), # Json, short please
                )

db.define_table('values',
                Field('device_id'),
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'),  # Name of variable
                Field('value', 'text'),  # Json, short please
                )


#########################################################################

## Adding table that should be used to store procedures on the server

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('user_email', 'string', required=True),
                Field('name', 'string')  # Name of procedure
                )

db.define_table('procedure_revisions',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                Field('last_update', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('stable', 'boolean', required=True) # True for stable False for not stable
                )

