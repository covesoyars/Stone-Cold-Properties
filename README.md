# Stone-Cold-Properties

### How to run the app on your computer while connecting to cloud sql:
  1. open stone_cold_props/stone_cold_props/settings.py and find the DATABASES dictionary around line 77
  2. change the port number to something higher than what it is
  3. go to root (stone_cold_props/) and run the command:
      ./cloud_sql_proxy -instances=database-258713:us-central1:instance-508=tcp:<SAME_PORT_NUMBER_IN_SETTINGS> -credential_file=keys/<NAME_OF_KEY_FILE> &
  4. Leave this running in background - this is the connection to the cloud
  5. still in root, run command python manage.py runserver
  
