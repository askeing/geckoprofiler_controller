PYTHON := python
VENV := .env-$(PYTHON)

# for travis

$(VENV)/bin/python:
	[ -d $(VENV) ] || $(PYTHON) -m virtualenv $(VENV) || virtualenv $(VENV)
	$(VENV)/bin/pip install --upgrade setuptools
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/python setup.py develop


.PHONY: dev-env
dev-env: $(VENV)/bin/python


# for testing
.PHONY: test
test: dev-env
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -Ur requirements.txt
	$(VENV)/bin/python -m unittest discover -s tests


.PHONY: clean
clean:
	find . -name "*.pyc" -type f -delete


# for document
.PHONY: docs
docs: dev-env clean
	$(VENV)/bin/pip install --upgrade epydoc
	rm -rf docs
	$(VENV)/bin/epydoc -o docs --html --exclude=test -v geckoprofiler_controller
