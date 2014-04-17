sslscout
========

About
-----
ssl configuration is an important but very complicated and ever changing topic. The complexity of configuring an ssl webserver correctly has lead to the creation of various ssl configuration checking services that help administrators get it right. The problem is that few admins remember to re-check their servers rating periodically. As new SSL vulnerabilities are found, or new and better ciphers are added, the best practices for running a secure ssl website changes, so the rating of a site can change at any time. sslscout is a web application where users can configure periodic checks of their websites using the various online ssl-configuration checking services. Users can configure automatic email notifications if/when the rating changes.


Service
-------
The service is under development. The latest revision of the master branch of https://github.com/tykling/sslscout/ is always running on https://dev.sslscout.com and eventually the production service will run on https://sslscout.com for all to use.


Install
-------
If you want to run your own instance of sslscout the source code is freely available under a BSD license. sslscout is a django application originally written for django 1.6. It also requires the django-registration and django-profile packages. To try it out just download the source and run it using djangos own webserver. To run it in production I use [http://projects.unbit.it/uwsgi/ uwsgi].


Configuration
-------------
Copy settings.py.dist to settings.py and change database and email server settings, and you should be good to go.


Questions
---------
- On IRC #sslscout on Freenode
- Make a github issue at https://github.com/tykling/sslscout/issues
- Send email to info@sslscout.com


Author
------
idea (oct. '13) and original code (april '14) by Thomas Steen Rasmussen / Tykling <thomas@gibfest.dk>
