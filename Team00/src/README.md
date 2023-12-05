### You can run file using the path. All files that will be generated will be saved in the `src` directory.
### Create virtual enviroment
```
python3 -m venv venv
```
### Install requirements
```
pip install -r requirements.txt
```
### Install and run Neo4j
```
docker pull neo4j:latest
docker run --name=neo4jtest -p=7474:7474 -p=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```
Open in browser
```
http://localhost:7474/
```
and login user: `neo4j` and set password: `password`.
### Enviroment variables
the following variables are stored in the `.env` file :
- FILE_WIKI - path to store file `wiki.json`
- URI - for neo4j
- USER_NAME - neo4j user name
- PASSWORD - neo4j password

Default values of environment variables:
```
WIKI_FILE="/../wiki.json"
URI="neo4j://localhost:7687"
USER_NAME="neo4j"
PASSWORD="password"
```
