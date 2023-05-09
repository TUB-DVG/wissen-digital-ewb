in this file a collection of tools and processes for backup prostgresql database
is stored

date: April 2022
author: Falk

# tools
- for the most backup tools the tools must be installed on the server (running db) and the local maschine (or better backup operating maschine)
## pgBackRest
- physical backups


## PgAdmin
- Gui-based: not handy solution for the server
- maybe not possible to put it into a crone job
- 



# tutorials
- https://www.youtube.com/watch?v=FU7eqwNCD-I
- https://djangocentral.com/backup-and-restore-data-in-postgresql/
- https://www.geeksforgeeks.org/postgresql-backup-database/
- https://www.postgresql.org/docs/9.1/backup.html

# backup strategy
- must be clear at beginning
- restore process is the focus, and backup is a part of the restore process

## physical backup
- make copy of the whole database system, like cp/rsync
- not possible to recover specific features or tables
- offline or online backups
- WAL = write-ahead log


- backup media folder local at the server:
```
rsync -rtp pyapps/webcentral/01_application/webcentral_app/media back_up_Media/

```
### tools (only open source)
#### Barman
  - https://pgbarman.org/
#### pgBackRest
  - https://pgbackrest.org/
  - 

## logical backup
- writes a file with php commands able to create the database as it was
- crossversion compatibility
- specific feature selection possible
### tools (only open source)
#### pg_dump
  - https://www.postgresql.org/docs/12/app-pgdump.html
  - command for a local dump: pg_dump -E UTF8 -U dbadmint -W -F p m4_data > ~/Desktop/m4_data_test7.sql
  - problem:
    - wrong encoding: especially when transfer database crossplattform
    
  - How To Fix - FATAL: Peer authentication failed for user "postgres" Error 
    - sudo vim /etc/postgresql/13/main/pg_hba.conf  ## 13 is the version number dump of
      - exchange peer to md5 im /etc/postgresql/13/main/pg_hba.con
```
      # Database administrative login by Unix domain socket
      local   all             postgres                                peer 

      # TYPE  DATABASE        USER            ADDRESS                 METHOD

      # "local" is for Unix domain socket connections only
      local   all             all                                     md5
      # IPv4 local connections:
      host    all             all             127.0.0.1/32            md5
      # IPv6 local connections:
      host    all             all             ::1/128                 md5
      # Allow replication connections from localhost, by a user with the
      # replication privilege.
      local   replication     all                                     peer
      host    replication     all             127.0.0.1/32            md5
<<<<<<< 02_work_doc/backup_db_howto.md
```
- sudo systemctl restart postgresql.service
- howto restore see [restore .sql](#psql-(restore-.sql))

=======
  - sudo systemctl restart postgresql.service
  - howto restore see [restore .sql](#psql-(restore-.sql))
>>>>>>> 02_work_doc/backup_db_howto.md
  - list existing databases:
    - sudo -u postgres psql > \l
#### postgres_dumpall
  - https://www.postgresql.org/docs/12/app-pg-dumpall.html
- both part of postgres installation
#### pg_restore
- cant used for plain dump files (.sql)
#### psql (restore .sql)
- the psql is a general postgres tool 
- restore at local maschine:
  1. create database via psql:
    1. start postgres terminal: 
    sudo -u postgres psql 
    2. command to create a database:
    postgres=# CREATE DATABASE m4_data2;
  2. command for restoring .sql-file:
  sudo -s psql -U dbadmint m4_data2 < ~/Desktop/m4_data_test5.sql
- Attention: Database and Django project have to be on the same status
## mixture 
- often used


# Django and postgresql data base
 
## Workflow databases and django 
1. dump database "A" and copy database "A"
2. copy migration files of database "A"
3. transfer database copy and copied migration (when needed)
  a) possible command
  scp: e.g. scp -r -i .ssh/id_rsa
  ubuntu@134.94.130.147:pyapps/webcentral/01_application/webcentral_app/tools_over
  ~/Desktop/Backup_db_server_20220707/mig_tool_over
4. migration file into the migration folder of the django app connected to database tables 
  a) only the 000XXX files not the init.py necessary
5. resort database "A" dump to a new data base including information from database "A"
- see above
6. load new data base into django project
- in settings.py
7. run makemigration
8. run migrate
9. check the database via pgAdmin or admin area of django

## Archiv 20220714
- outcome talk with a friend of Falk
  - is it important to copy the migration file for the specific data base
  - django is clever regarding changes in database structure because of changes
    in the manage.py(s), but the migration-file of the database must be there
  - migration-files are important
- [x] check this idea
  - [x] remove migration file from gitignore, check the migration file again
  - [x] Backup local migration-file to Desktop/Backup_migrations_main_Schlag1_temp
  - [x] delete old/backuped migration files
  - [x] copy the migration files from the server into my local branch main_Schlag1_temp
  - [x] test makemigration with the copy of the database from the server
    - makemigration, migrate > check admin area and also pgadmin, database looks like it should, new table is there
