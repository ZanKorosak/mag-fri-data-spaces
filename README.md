# FRI-LDS-Uploader
This Fastapi implementation will allow you to batch upload multiple CSV files in a more optimized way. In current version of the connector (branch 0.90prod, version v2.0.0-beta), this is only possible for JSON-LD assets, but not raw CSV datasets, which can be then turned into assets on the connector UI.

This installation was tested on Ubuntu 22, using different OS will most likely mean you have to install pip packages and python virtual env in a different way.


## Prerequisites
1. You registered for LDS access and got accepted on https://language-data-space.eu/registryui/
2. You deployed and registered your LDS connector, using the provided documentation from LDS
3. You created an account on your organization connector (any LDS realm)



## Installation process
1. Create a `.env` file in project root, and insert your username and password from your connector (step 3 in prerequisites)
```
KEYCLOAK_USERNAME="<USERNAME>"
KEYCLOAK_PASSWORD="<PASSWORD>"
```
2. Make sure you have installed required apt packages to enable pip module installation. 
```
apt install pip
apt install python3.11-venv
```

### Make a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the Fastaspi server

CLI: 
```
fastapi dev src --port 9009 --host 0.0.0.0
```

Docker compose: 
```

docker compose up -d --build --force-recreate
```


### Docs available on 
`http://lds.cjvt.si:9009/docs#/` (HTTP only)
