clean_pyc:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete

build:
	python setup.py sdist

release:
	python setup.py sdist upload

test:
	pytest --cov-report html --cov=telega_compose

sinclude makefile-local
