import datetime

#########################################################################

## Adding table that should be used to store procedures on the server

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('user_id', 'string', required=True),
                Field('name', 'string')  # Name of procedure
                )

db.define_table('procedure_revisions',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('procedure_data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                Field('last_update', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('stable_version', 'boolean', required=True) # True for stable False for not stable
                )

