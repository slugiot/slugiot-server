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
                Field('level', 'integer'),  # int, 0 = most important.
                Field('message', 'text'),
                )

db.define_table('output',
                Field('device_id'),
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'),  # Name of variable
                Field('value', 'text'),  # Json, short please
                )

db.define_table('values',
                Field('device_id'),
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'),  # Name of variable
                Field('value', 'text'),  # Json, short please
                )

#########################################################################
#These correspond to authentication tables.
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)

## after auth = Auth(db)

db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('email', length=128, default='', unique=True),  # required
    Field('password', 'password', length=512,  # required
          readable=False, label='Password'),
    Field('address'),
    Field('city'),
    Field('phone'),
    Field('registration_key', length=512,  # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,  # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,  # required
          writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name]  # get the custom_auth_table
custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table  # tell auth to use custom_auth_table


## before auth.define_tables()
auth.define_tables()

#########################################################################
#These conrespond to device tables.
#########################################################################

db.define_table(
    "Device_Table",
    Field("device_id", length=128, default=''),  # required
    Field("owner_email", length=128, default=''),  # required
    Field("name", length=128, default=''),  # required
    Field("description", length=512, default='')
)
device_table = db["Device_Table"]  # get the custom_auth_permission_table
device_table.device_id.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
device_table.owner_email.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
device_table.name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
