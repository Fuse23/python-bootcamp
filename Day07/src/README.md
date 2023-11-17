## Create and activate virtual enviroment
```
python3 -m venv venv
source venv/bin/activate
cd src
pip install -r requirements.txt
```

## Run Voight Kampff test
```
python voight_kampff_test/main.py
```

## Test rules
1. Each question has 3 answer (test has 10 questions).
2. After each response you need to enter your condition:
    - Respiration (measured in BPM, normally around 12-16 breaths per minute)
    - Heart rate (normally around 60 to 100 beats per minute)
    - Blushing level (categorical, 6 possible levels)
    - Pupillary dilation (current pupil size, 2 to 8 mm)

## Run tests
```
pytest
```
You also can use `-v` flag for more informations about tests.

For check tests coverage:
```
pytest --cov=voight_kampff_test --cov-report=html
```

## Generate documentation
```
cd docs
make html
```
You can also regenerate documentation
```
cd src
sphinx-apidoc -o docs/source voight_kampff_test
```

## Viwe documentation and tests coverage
```
cd ..
python -m http.server
```
Documentation: `localhost:8000/docs/build/html/index.html`

Tests coverage: `localhost:8000/htmlcov/index.html`

