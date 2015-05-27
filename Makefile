install:
	pip install -e .[dev] --upgrade
	pip install tox

test:
	coverage erase
	tox
	coverage html
