## Create and activate virtual enviroment
```bash
python3 -m venv venv
source venv/bin/activate
cd src
pip install -r requirements.txt
```
## Run EX00
```bash
cd EX00
python fight.py
```
### Run test
```bash
pytest
```
## Run EX01
```bash
cd ../EX01
python server.py
```
In new terminal
```bash
source venv/bin/activate
cd src/EX01
python crawl.py post http://example.com
python crawl.py get <returned id>
```
`crawl.py` with *post* return json with field **id**

`crawl.py` with *get* and **id** return task

You can try all mothod in browser, open `loclahost:8888/docs`

### Run test
```bash
pytest
```

## Run EX02
First off all, run redis
```bash
cd ../EX02
python server_cached.py 30
```
`server_cached.py` gets argument *time* it's a time that the cache will be stored

In new terminal
```bash
source venv/bin/activate
cd src/EX01
python crawl.py post http://example.com
python crawl.py get <returned id>
```
You can try all mothod in browser, open `loclahost:8888/docs`
