Here, the workflow of merging changes into the main branch.

author: Falk
date: 2022 July

# local preparation
1. create new branch based on the actual main branch
1. set up database according to the main branch
   a) copy database from https://tubcloud.tu-berlin.de/apps/files/?dir=/Shared/Digitale_Vernetzung/Assis/03_Projekte/DVG0001_BMWi_Wende/08_gemeinsames_Arbeiten/09_Wissensplattform_M4/01_Backup_Server_DB&fileid=3323429959
   b) resorte database to local postresql server see [resorte .sql](./backup_db_howto.md#### psql (restore .sql))
   c) adapt database setup in settings.py
   d) check database works correctly
2. check the right migartion file are loaded
- should be the case, when pulled from repo
3. result: main branch content ("main_temp") including the fitting db is setup
# transfer or make change into the "main_temp"
1. use cherry picking method or copy file
2. check changes local
# check "main_temp" at server
1. checkout and pull "main_temp" 
2. check especially the new feature
# merge "main_temp" with main branch
- I use merge request function at gitlab
# test main branch local
# use main branch at server
1. checkout and pull main branch
