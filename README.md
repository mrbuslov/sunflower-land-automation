# DISCLAIMER:
My 2 accounts are banned for "bot activity", so I need contributors to look through Sunflower Land's official UI github repo and find additional requests that their front sends to back
I DO NOT reccomend using it for now, bc 99% your account will be blocked. Need more work to be done
To make contributions, please, create PR

# How to run

## Create environment
```
python -m venv venv 
OR 
PYENV_VERSION=3.11.6 python -m venv venv

. venv/bin/activate
pip install -r requirements.txt
```

## Gather everything
```
PYTHONPATH=. python scripts/gather_all.py
```

## Planting
All available crops are listed in `utils/plants_schemas.py`
```
PYTHONPATH=. python resources_gathering/plant.py "Sunflower Seed" 10
OR
PYTHONPATH=. python resources_gathering/plant.py "Sunflower Seed"
```

## Harvesting
```
PYTHONPATH=. python resources_gathering/harvest.py
OR 
PYTHONPATH=. python resources_gathering/harvest.py "Sunflower Seed"
```

## Automatic planting n harvesting
```
PYTHONPATH=. python scripts/plant_n_harvest.py
```

## Cutting down trees
```
PYTHONPATH=. python resources_gathering/trees_cut.py
```


# Useful commands

## Update `session.json` file
Note: if you have `SHOULD_REFRESH_SESSION=False`, use this to update session file:
```
PYTHONPATH=. python settings/update_session.py
```

# TODO:
- replace requests with httpx

# WIP (work in progress)
All information below is in progress

## Auto Planting and Harvesting (in past)
Before running script, identify, if you have `config/crops_operations.json`. If you have, skip these step. If NOT - you MUST do these steps:
- `PYTHONPATH=. python resources_gathering/plant.py "Sunflower Seed" 1` Instead of "Sunflower Seed" can be any other seed
- wait 1 minute
- `PYTHONPATH=. python settings/update_session.py`
- `PYTHONPATH=. python resources_gathering/harvest.py` Instead of "Sunflower Seed" can be any other seed  
- `PYTHONPATH=. python settings/update_session.py`
- wait enough time for hypothetical seeds to grow (ex. If you have 100 sunflower seeds overall, 20 holes. Wait (100 / 20) * 1 minute to grow = 4 minutes). Because you run it in the past, you MUST make sure you reserved enough time.

Great! Now you're ready to go!
```
PYTHONPATH=. python resources_gathering/plant_n_harvest.py "Sunflower Seed"
```
