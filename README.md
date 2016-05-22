# Lister

## Info
This is a self hosted application that is used to create and manage lists.  It uses Python, the Django web framework, and a relational database.  Openshift action hooks and a database example are also provided for easy deployment!

# Setup

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
