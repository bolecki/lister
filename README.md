# Lister

## Info
This is a self hosted application that is used to create and manage lists.  It uses Python, the Django web framework, and a relational database.  Openshift action hooks and a database example are also provided for easy deployment!

# Setup
Skip down to the openshift section if you would like to run the application from openshift.

## Clone and Generate Key
These steps will clone the repository and generate a new secret key.

```bash
# Clone the repo
git clone https://github.com/bolecki/lister.git

# Change directory into the repo
cd lister/

# Generate a secret key
python .openshift/action_hooks/gen_key.py

# Check to make sure key was generated
cat lister/lister/secrets.py
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

## Install Requirements
This step will install the required dependencies.  It is recommended to run these steps and the application from a virtualenv.

```bash
pip install -r requirements.txt
```

## Configuration
Make any necessary configuration changes within the lister/lister/settings.py file.  This is where installed apps, database configuration, etc are handled.

## Run the App
Once the database is configured and running, simply start the webserver!  This is currently for development use only.  Ultimately this should be served with a full webserver such as Apache or Nginx.

Change the listening ip and port as needed, ie 127.0.0.1:80.

```bash
# Change directory to the Django project
cd lister

# Run HTTP server
nohup python manage.py runserver 0.0.0.0:8080 &

# Alternatively, run HTTPS server instead
nohup python manage.py runsslserver 0.0.0.0:8080 &
```

## Openshift
To run this application under openshift, simply create a new application with a Django cartridge.  Set the source code to this repository, "https://github.com/bolecki/lister.git", and optionally select scaling.

From the rhc client, set the wsgi app environment variable to point to the Django wsgi.py file.  The full path will depend on the app uuid.  Make sure to replace the appname and uuid in the final command.

```bash
# Grab the uuid
rhc domain show | grep uuid
appname @ http://appname-domain.rhcloud.com/ (uuid: xxxxxxxxxxxxxxxxxxxxxxxx)

# Set the env variable
rhc env set OPENSHIFT_PYTHON_WSGI_APPLICATION='/var/lib/openshift/xxxxxxxxxxxxxxxxxxxxxxxx/app-root/repo/lister/lister/wsgi.py' --app appname

# Reload the app
rhc app reload appname
```

Add a Postgresql gear at any time with the default settings.py file to have the new database automatically detected!

# TODO
1. Instructions for Apache/Nginx configuration
2. Add more api endpoints
3. Add more list types
4. ~~Handle CSRF tokens~~
5. Add test cases
6. Add travis CI integration
