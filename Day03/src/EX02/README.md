## Installing ansible
### Insatalling pipx
- On macOS
```
brew install pipx
pipx ensurepath
```
- On Linux
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
### Installing ansible
```
pipx install --include-deps ansible
```
## Running ansible test for the generated file
```
ansible-playbook path-to-file --check
```
### Possible paths
```
./src/EX02/deploy.yml
./EX02/deploy.yml
./deploy.yml
```
### Additional flags:
- `-K` for running by sudo user
- `-vvv` for detailed output