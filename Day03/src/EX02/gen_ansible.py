import yaml
import os


start_path: str = os.path.dirname(__file__) + '/'
materaials_path: str = os.path.join(start_path, '../../materials/')
ex00_path: str = os.path.join(start_path, '../EX00/')
ex01_path: str = os.path.join(start_path, '../EX01/')
with open(materaials_path + 'todo.yml', 'r') as file:
    todo = yaml.load(file, yaml.FullLoader)
deploy = [{
    'name': 'Playbook',
    'hosts': 'localhost',
    'become': 'yes',
    'tasks': [
        {
            'name': 'Installation packeges',
            'ansible.builtin.apt': {
                'name': '{{ item }}'
            },
            'loop': todo['server']['install_packages'],
        },
        {
            'name': 'Copying files',
            'ansible.builtin.copy': {
                'src': '{{ item.src }}',
                'dest': '{{ item.dest }}',
            },
            'loop': [
                {
                    'src': ex00_path + 'exploit.py',
                    'dest': start_path + 'exploit.py',
                },
                {
                    'src': ex01_path + 'consumer.py',
                    'dest': start_path + 'consumer.py'
                },
            ]
        },
        {
            'name': 'Run files',
            'ansible.builtin.shell': {
                'cmd': '{{ item.cmd }}',
            },
            'loop': [
                {
                    'cmd': 'python3 exploit.py',
                },
                {
                    'cmd': 'python3 consumer.py -e ' + ','.join(todo['bad_guys'])
                },
            ],
        },
    ],
}]
with open(start_path + 'deploy.yml', 'w') as file:
    yaml.dump(deploy, file, sort_keys=False, default_flow_style=False)
