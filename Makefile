.PHONY: install
install:
	@export PIP_DEFAULT_TIMEOUT=7200
	@pip install wheel; pip install --upgrade pip
	@pip install pipenv
	@export PIPENV_VENV_IN_PROJECT=true
	@export PIPENV_TIMEOUT=7200
	@pipenv sync --dev


.PHONY: install-lock
install-lock:
	@export PIP_DEFAULT_TIMEOUT=7200
	@pip install wheel; pip install --upgrade pip
	@pip install pipenv
	@export PIPENV_VENV_IN_PROJECT=true
	@export PIPENV_TIMEOUT=7200
	@pipenv lock
	@pipenv install --dev


.PHONY: test
test:
	@# sudo apt install graphviz
	@pipenv run pytest -v --durations=0 --failed-first --maxfail=1 \
	 --cov=kaipred --cov-report=term-missing --profile-svg


.PHONY: test-nosvg
test-nosvg:
	@pipenv run pytest -v --durations=0 --failed-first --maxfail=1 \
	 --cov=kaipred --cov-report=term-missing


.PHONY: test-file
test-file:
	@pipenv run pytest tests/test_${file}.py -v --durations=0 --failed-first --maxfail=1 \
	 --cov=kaipred --cov-report=term-missing


# https://github.com/sphinx-doc/sphinx/issues/3382
.PHONY: sphinx
sphinx:
	@# sudo apt install pandoc
	@pandoc --from markdown --to rst README.md -o docs/README.rst
	@#pandoc --from markdown --to rst .github/CONTRIBUTING.md -o docs/CONTRIBUTING.rst
	@#pandoc --from markdown --to rst docs/markdown/INSTALLATION.md -o docs/INSTALLATION.rst
	@# When new module was added, update docs/covsirphy.rst and docs/(module name).rst
	@sphinx-apidoc -o docs covsirphy
	@cd docs; pipenv run make html; cp -a _build/html/. ../docs
	@rm -rf docs/_modules
	@rm -rf docs/_sources


# https://github.com/sphinx-doc/sphinx/issues/3382
.PHONY: docs
docs:
	@rm -rf docs/_images
	@rm -f docs/*ipynb
	@# docs/index.rst must be updated to include the notebooks
	@#pipenv run runipy example/usage_quick.ipynb docs/usage_quick.ipynb
	@make sphinx


.PHONY: example
example:
	@pipenv run ./main.py setup --user demo

.PHONY: pypi
pypi:
	@rm -rf covsirphy.egg-info/*
	@rm -rf dist/*
	@pipenv run python setup.py sdist bdist_wheel
	@pipenv run twine upload --repository pypi dist/*


.PHONY: test-pypi
test-pypi:
	@pandoc --from markdown --to rst README.md -o README.rst
	@rm -rf covsirphy.egg-info/*
	@rm -rf dist/*
	@pipenv run python setup.py sdist bdist_wheel
	@pipenv run twine upload --repository testpypi dist/*


.PHONY: clean
clean:
	@rm -rf input
	@rm -rf prof
	@rm -rf .pytest_cache
	@find -name __pycache__ | xargs rm -r
	@rm -rf example/output
	@rm -rf dist covsirphy.egg-info
	@rm -f README.rst
	@rm -f .coverage*
	@pipenv clean || true


.PHONY: update
update:
	@export PIP_DEFAULT_TIMEOUT=7200
	@export PIPENV_VENV_IN_PROJECT=true
	@export PIPENV_TIMEOUT=7200
	@pipenv update --outdated


.PHONY: cache_clear
cache_clear:
	@# Try this command when failed in locking
	@# https://pipenv.kennethreitz.org/en/latest/diagnose/
	@export PIPENV_VENV_IN_PROJECT=true
	@export PIPENV_TIMEOUT=7200
	@pipenv lock --clear

.PHONY: rm
rm:
	@pipenv --rm
