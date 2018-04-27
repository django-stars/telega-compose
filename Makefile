clean_pyc:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete

build:
	python setup.py sdist

release:
	python setup.py sdist upload

sinclude makefile-local
