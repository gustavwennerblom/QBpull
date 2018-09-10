# QBpull - moving Questback survey responses to a database

Questback EFS provides a good end-user experience and a very powerful 
configuration options for administrators. The reporting interface
is however not accessible for non-admin users without purchasing
additional reporting modules. The "old style" SOAP interface is not
compatible with modern REST-consuming analytics platforms.  

Storing the survey results in a standard
RDBMS (in the default case MSSQL) allows for the data to be loaded
and analysed in reporting tools other than the Questback proprietary
solutions.

## Key components
There are three main module sets forming this solution
* **qbpull.py** - This module defines an interface to Questback EFS, and
makes it possible to extract survey responses as a csv (and some
other utility functions). It utilizes [Zeep](https://github.com/mvantellingen/python-zeep) 
for handling the SOAP interface.
* **dbmanager.py** and **models.py** defines the database structure
where the service stores parsed data from **qbpull**
* **main.py** strings together the two modules above and structures
the data flow

## Supporting components
In addition, the service makes use of:
* **Alembic** for database setup and migrations. The *alemic* folder contains
all database migrations
* **mailer.py** is a supporting module that distributes a log file after
each execution of the script via e-mail. The version in this repo is
preparet to use with [Amazon SES](https://aws.amazon.com/ses/)

## Configuration
* The module **config.py** contains a set of configuration variables
that the service requires to function properly.
* The service also expects a set of credentials for the Questback API,
the target database, and the credentials for the SMTP server (if 
using *mailer.py*)


