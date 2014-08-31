install:
	pip install -e .[dev] --upgrade

test:
	python example/basic_project/manage.py test gcm

coverage:
	coverage erase
	coverage run example/basic_project/manage.py test gcm
