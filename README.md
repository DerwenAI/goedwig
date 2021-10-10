A generic query engine for graph data, based on abstract syntax trees as input.


## Install

```
python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt
```


## Run example

```
python3 sample.py
```


## Build setup

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

Then initialize the tag-based versioning:
```
TAG=$(git tag | sort -r | head -1)
echo "'git tag'" > goedwig/tag.py
echo "TAG = '$TAG'" >> goedwig/tag.py
```


## Package release

```
python3 setup.py install --dry-run
./bin/push_pypi.sh
```


## About the name

The name [`goedwig`](https://glosbe.com/cy/cy/goedwig) is Welsh/Gymraeg –
pronounced `/ˈɡɔi̯dwɪɡ/` –
which means ["forest"](https://en.wiktionary.org/wiki/coedwig).
Herein we parse many trees.
