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
                Field('device_id', required=True),  # not sure what field type this should be
                Field('name', 'string'),  # Name of procedure
                Field('data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                # last_update corresponds to any save
                Field('last_update', 'datetime', default=datetime.datetime.utcnow(), required=True),
                # last_update_stable corresponds to an entry that is ready to be sent to client
                Field('last_update_stable', 'datetime', default=datetime.datetime.utcnow(), required=True)
                )
