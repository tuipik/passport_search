# Void passport checker
***A simple app for checking void documents.***

---
**Usage**

- Clone this repository via http `git clone https://github.com/tuipik/passport_search.git`
or via ssh `git clone git@github.com:tuipik/passport_search.git`

- In terminal open directory with source code of repo

- Create env and start it `python3.7 -m venv env && source env/bin/activate`

- Install requirements `pip install -r requirements.txt`

- Migrate db `make migrate`  This command also creates superuser with login `admin` and pass `adminpass`

- Fill up database with data `make db`  This may take about 1 hour cause data has more than 2 mln rows

- Start local server by `make run` command in Terminal

---
**Endpoints:**


for web search app: `http://0.0.0.0:8000/`

    - example of dockument: HA 681035
    
for admin: `http://0.0.0.0:8000/admin`

for api search: `http://127.0.0.1:8000/api/v1/find_documents/`

---
**Postman Collection:**

`https://www.getpostman.com/collections/26c743fed3655fa9f020`