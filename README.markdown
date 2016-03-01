## Readme

web2py is a free open source full-stack framework for rapid development of fast, scalable, secure and portable database-driven web-based applications. 

It is written and programmable in Python. LGPLv3 License

Learn more at http://web2py.com

Clone this repository via: 

    git clone --recursive https://github.com/lucadealfaro/web2py.git

The --recursive option is important, or else you will be missing PyDAL, the database abstraction layer. 

## Google App Engine deployment

This is a special version of web2py, with logging written to mesh well with the logging on Google Appengine.
To deploy, edit examples/app.yaml to replace "yourappname" with your application id. 

### Creating a new app

To create a new app called myapp:

    cd web2py/applications
    cp -r welcome myapp
    
You may also want to edit routes.py to define what is your default app; replace "welcome" with "myapp".

### Running the app.

You can either use the Google Appengine Launcher, or you can download the Google Appengine source SDK and do:

    python dev_appserver.py web2py/

## Documentation (readthedocs.org)

[![Docs Status](https://readthedocs.org/projects/web2py/badge/?version=latest&style=flat-square)](http://web2py.rtfd.org/)

## Tests

[![Build Status](https://img.shields.io/travis/web2py/web2py/master.svg?style=flat-square&label=Travis-CI)](https://travis-ci.org/web2py/web2py)
[![MS Build Status](https://img.shields.io/appveyor/ci/web2py/web2py/master.svg?style=flat-square&label=Appveyor-CI)](https://ci.appveyor.com/project/web2py/web2py)
[![Coverage Status](https://img.shields.io/codecov/c/github/web2py/web2py.svg?style=flat-square)](https://codecov.io/github/web2py/web2py)


## Installation Instructions

To start web2py there is NO NEED to install it. Just unzip and do:

    python web2py.py

That's it!!!

## web2py directory structure

    project/
        README
        LICENSE
        VERSION                    > this web2py version
        web2py.py                  > the startup script
        anyserver.py               > to run with third party servers
        ...                        > other handlers and example files
        gluon/                     > the core libraries
            packages/              > web2py submodules
              dal/
            contrib/               > third party libraries
            tests/                 > unittests
        applications/              > are the apps
            admin/                 > web based IDE
                ...
            examples/              > examples, docs, links
                ...
            welcome/               > the scaffolding app (they all copy it)
                ABOUT
                LICENSE
                models/
                views/
                controllers/
                sessions/
                errors/
                cache/
                static/
                uploads/
                modules/
                cron/
                tests/
            ...                    > your own apps
        examples/                  > example config files, mv .. and customize
        extras/                    > other files which are required for building web2py
        scripts/                   > utility and installation scripts
        handlers/
            wsgihandler.py         > handler to connect to WSGI
            ...                    > handlers for Fast-CGI, SCGI, Gevent, etc
        site-packages/             > additional optional modules
        logs/                      > log files will go in there
        deposit/                   > a place where web2py stores apps temporarily

## Issues?

Report issues at https://github.com/web2py/web2py/issues
