## Create and activate virtual enviroment
```
python3 -m venv venv
source venv/bin/activate
cd src
pip install -r requirements.txt
python -m pip install --editable ./
```
## Generate files from proto file
Тot necessary as the files are already in the repository
```
cd proto
python -m grpc_tools.protoc --proto_path=. ./galaxy.proto --python_out=. --grpc_python_out=. --pyi_out=.
```
## Run EX00
```
cd EX00
python reporting_server.py
```
In new terminal
```
python reporting_client.py 1234.5 5432.1 6789 9876
```
## Run EX01
`Don't stop the server`

Server dosen't often genetare a valid response =(

Run script several times
```
cd EX01
python reporting_client_v2.py 1234.5 5432.1 6789 9876
```
## Run EX02
```
cd ../EX02
```
Create `.env` file with the following content for connect to Postgresql:
```
DB_USER=your_user_name
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database_name
```
Create database use script
```
python ./create_db.py
```
Use migration for create tables
```
alembic upgrade fec5f6ca3ad1
```
`Don't stop the server`

Server dosen't often genetare a valid response =(

Run script several times
```
python ./reporting_client_v3.py 1234.5 5432.1 6789 9876
```
`Now you can stop the server =)`
