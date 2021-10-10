A generic query engine for graph data, based on abstract syntax trees as input.


## Install

```
python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt
```


## Run

```
python3 sample.py
```


## Build

```
python3 -m pip install -U pip setuptools wheel
python3 -m pip install -r requirements-dev.txt
```

We use *pre-commit hooks* based on [`pre-commit`](https://pre-commit.com/)
and to configure that locally:
```
pre-commit install
git config --local core.hooksPath .git/hooks/
```


## About the name

The name [`goedwig`](https://glosbe.com/cy/cy/goedwig) is Welsh/Gymraeg –
pronounced `/ˈɡɔi̯dwɪɡ/` –
which means ["forest"](https://en.wiktionary.org/wiki/coedwig).
Herein we parse many trees.
