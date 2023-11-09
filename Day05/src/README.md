# Day05
## Requirements
- Python 3.10 or higher
- Create virtual enviroments
## Create and activate virtual enviroments
```
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```
## EX00
```
python src/EX00/credentials.py
```
In new terminal test with `curl`
```
curl http://127.0.0.1:8888/?species=Time%20Lord
```
return `{"credentials": "Rassilon"}`
or use tests
```
python src/EX00/tests.py
```
output: Link, HTTP Header, Content

## EX01
Run Flask app
```
python src/EX01/server/app.py
```
Open `http://localhost:8888/`. Click on button `Select file` and select any music file 
or from the directory `src/EX01/materials`, then click `Send`.

Files with the same name are used as sources for the same audio on the page.

In new terminal

Show all uploaded files
```
python src/EX01/client/screwdriver.py list
```
Upload new file
```
python src/EX01/client/screwdriver.py upload 'path-to-file'
python src/EX01/client/screwdriver.py upload src/EX01/materials/Playboi_Carti-Magnolia.mp3
```

## EX02
```
python src/EX02/doctors.py
```
