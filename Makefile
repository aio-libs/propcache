# Thin wrappers around ``tox``. The Python-aware automation lives in
# ``tox.ini`` (see the header comments there for a tour of the envs).
# The targets below exist so habitual ``make <foo>`` invocations keep
# working — but feel free to call ``tox -e <env>`` directly.

TOX ?= tox

# Default Python factor for the local test envs. Override on the
# command line (e.g. ``make test PY=py311``) when you want to test
# against a different interpreter.
PY ?= py312

# Tox factor controlling whether the C-extension is built. Either
# ``compiled`` (default; exercises the accelerated build) or ``pure``.
VARIANT ?= compiled


all: test


.PHONY: cythonize
cythonize:
	$(TOX) -e cython


.PHONY: fmt lint
fmt lint:
	$(TOX) -e lint


.PHONY: test
test:
	$(TOX) -e $(PY)-$(VARIANT)


.PHONY: vtest
vtest:
	$(TOX) -e $(PY)-$(VARIANT) -- -v


.PHONY: cov
cov:
	$(TOX) -e $(PY)-$(VARIANT) -- --cov-report=html --cov-report=term
	@echo "python3 -Im webbrowser file://`pwd`/htmlcov/index.html"


.PHONY: doc
doc:
	$(TOX) -e docs
	@echo "python3 -Im webbrowser file://`pwd`/.tox/docs/html/index.html"


.PHONY: doctest
doctest:
	$(TOX) -e doctest


.PHONY: doc-spelling
doc-spelling:
	$(TOX) -e spelling


.PHONY: build-dists
build-dists:
	$(TOX) -e build-dists


# Provision an editable venv at ``./venv`` mirroring the default test
# env. Reproduces the previous ``make .develop`` workflow.
.PHONY: develop
develop:
	$(TOX) devenv -e $(PY)-$(VARIANT) venv
