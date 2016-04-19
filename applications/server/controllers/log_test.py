# tesing logs database

# add random log data by populate
from gluon.contrib.populate import populate
db.logs.truncate()
db.outputs.truncate()
populate(db.logs, 50)
populate(db.outputs, 50)

# add fake testing data
db.define_table('Kitchen',
                Field('Temperature', 'double'))

db.define_table('Living_room',
                Field('Temperature', 'double'))

db.Kitchen.Temperature.requires = IS_INT_IN_RANGE(30, 45)
db.Living_room.Temperature.requires = IS_INT_IN_RANGE(20, 35)
db.Kitchen.truncate()
db.Living_room.truncate()
populate(db.Kitchen, 100)
populate(db.Living_room, 100)
k_temp = db().select(db.Kitchen.Temperature)
l_temp = db().select(db.Living_room.Temperature)

def log_report():
    grid = SQLFORM.grid(db.logs, deletable=False, editable=False,
                             create=False, paginate=50, formstyle='table3cols')
    # write fake temperature data to a csv file
    import csv
    with open('./applications/server/static/temper.csv', 'wb') as csvfile:
        tmpwriter = csv.writer(csvfile, delimiter=',')
        tmpwriter.writerow(['data','Kitchen','Living_room'])
        for i in range(len(k_temp)):
            tmpwriter.writerow([str(i),str(k_temp[i].Temperature),str(l_temp[i].Temperature)])

    return dict(grid=grid)
