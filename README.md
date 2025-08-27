# Prereqs
```
apt install pip
apt install python3.11-venv
pip install "fastapi[standard]"
```

# Make venv
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Run with fastapi CLI
`fastapi dev src --port 9009 --host 0.0.0.0`


# Docs available on 
`http://lds.cjvt.si:9009/docs#/`


# Run with docker compose
```
docker-compose up -d --build --force-recreate
```
