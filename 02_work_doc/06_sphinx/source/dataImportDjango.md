# Data-Import

This document describes the different ways to import data into the webcentral-database.
In general, data can be imported using the following ways:
    
    - Using the django-admin panel.
    - Using the custom django `data_import` command.
    - Using a SQL-dump.

In the followin sections these methods are described in detail.

## Data-import using the django admin panel
This approach can be considered straight forward. If only small chunks of data need to be imported this method is apropriate. For that method to work, the django superuser-credentials are needed, which can be found in the `.env`-file in the root project folder.
The admin panel can be entered by either opening your locally hosted version or the server hosted production version. For your local version enter the following link in your browser of choice:
```
http://127.0.0.1:8000/admin
```
On the opened site, enter username and password from the `.env`-file. You should then be able to create, modify or delete 
