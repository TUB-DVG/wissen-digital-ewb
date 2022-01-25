Here it is described how to run python
stuff at the server.

The example here used server IK10 put data into
the data base.

# general steps
- connect via ssh

# run ipython at server
## install ipython

## run
- activate enviroment via the source command: source
  /home/ubuntu/pyapps/ve_wc/bin/activate
- run shell plus 
  - ./manage.py shell_plus --ipython
  - django-extensions needed
- stop ipython shell
  - quit
  
  
# run script bring data into data base
- %run project_listing/data_import.py
