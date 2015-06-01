install:
	pip install -e .[dev] --upgrade --process-dependency-links
	pip install tox

test:
	coverage erase
	tox
	coverage html
