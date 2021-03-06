
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
MODULE := vaskitsa
VERSION := $(shell awk '/^version =/ {print $$3}' pyproject.toml)
SPHINX_FLAGS := -b html ./docs public
SPHINX_WEBSITE_FLAGS := --port 8100 --host localhost --open-browser --watch ${MODULE}

all: lint test

clean:
	@rm -rf build dist .DS_Store .pytest_cache .cache .eggs .coverage .tox coverage
	@find . -name '__pycache__' -print0 | xargs -0 rm -rf
	@find . -name '*.egg-info' -print0 | xargs -0 rm -rf
	@find . -name '*.pyc' -print0 | xargs -0 rm -rf

build:
	python setup.py build

doc-devel:
	export PYTHONPATH=${ROOT_DIR}
	vaskitsa documentation generate ${ROOT_DIR}
	sphinx-autobuild ${SPHINX_WEBSITE_FLAGS} ${SPHINX_FLAGS}

doc:
	export PYTHONPATH=${ROOT_DIR}
	vaskitsa documentation generate ${ROOT_DIR}
	sphinx-build ${SPHINX_FLAGS}

lint:
	tox -e lint

test:
	tox -e unittest

upload: clean
	python3 setup.py sdist
	twine upload dist/*

tag-release:
	git tag -a ${VERSION} -m "Publish release ${VERSION}"
	git push origin ${VERSION}

.PHONY: all test
