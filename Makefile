PYXS = $(wildcard src/propcache/*.pyx)
SRC = propcache tests

all: test


.install-deps: $(shell find requirements -type f)
	pip install -U -r requirements/dev.txt
	pre-commit install
	@touch .install-deps


.install-cython: requirements/cython.txt
	pip install -r requirements/cython.txt
	touch .install-cython


src/propcache/%.c: src/propcache/%.pyx
	python -m cython -3 -o $@ $< -I src/propcache


.cythonize: .install-cython $(PYXS:.pyx=.c)


cythonize: .cythonize


.develop: .install-deps $(shell find src/propcache -type f)
	@pip install -e .
	@touch .develop

fmt:
ifdef CI
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif

lint: fmt

test: lint .develop
	pytest


vtest: lint .develop
	pytest -v


cov: lint .develop
	pytest --cov src/propcache --cov-report html --cov-report term
	@echo "python3 -Im webbrowser file://`pwd`/htmlcov/index.html"


doc: doctest doc-spelling
	make -C docs html SPHINXOPTS="-W -E --keep-going -n"
	@echo "python3 -Im webbrowser file://`pwd`/docs/_build/html/index.html"


doctest: .develop
	make -C docs doctest SPHINXOPTS="-W -E --keep-going -n"


doc-spelling:
	make -C docs spelling SPHINXOPTS="-W -E --keep-going -n"
