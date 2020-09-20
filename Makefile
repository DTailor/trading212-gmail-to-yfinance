-include .env

.PHONY : help

PY_VERSION = 3.8.5

install:
	poetry env use ${PY_VERSION}
	poetry install --no-dev

install-dev:
	poetry env use ${PY_VERSION}
	poetry install

reinstall-dev:
	poetry env remove ${PY_VERSION} || true
	make install-dev