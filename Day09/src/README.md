## Create and activate virtual enviroments

```bash
python3 -m venv venv
source venv/bin/activate
cd src
pip install -r reqirements.txt
```

## Run EX00

```bash
cd EX00
python setup.py install
python test.py
```

## Run EX01

```bash
cd ../EX01
python monotonic.py
```

## Run EX02

```bash
cd ../EX02
python setup.py build_ext --inplace
python test_mul_perf.py
```
