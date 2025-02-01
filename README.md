# How to run

## Create environment
```
python -m venv venv 
OR 
PYENV_VERSION=3.11.6 python -m venv venv

. venv/bin/activate
pip install -r requirements.txt
```

## Planting
```
PYTHONPATH=. python resources_gathering/plant.py "Sunflower Seed" 10
```

## Harvesting
```
PYTHONPATH=. python resources_gathering/harvest.py
```
