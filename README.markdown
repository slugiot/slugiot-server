## Readme

SlugIOT is a remote device management system for small embedded linux systems.
This is the code that runs on the server.

Clone this repository via: 

    git clone --recursive https://github.com/slugiot/slugiot-server.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Google App Engine deployment

This is a slightly modified version of web2py, with logging written to mesh well with the logging on Google Appengine.
To deploy, edit examples/app.yaml to replace "yourappname" with your application id. 

### Running the app.

#### Running the app locally emulating Google Appengine

You can either use the Google Appengine Launcher, or you can download the Google Appengine source SDK and do:

    python dev_appserver.py web2py/
    
#### Running the app using web2py

    python web2py/web2py.py

