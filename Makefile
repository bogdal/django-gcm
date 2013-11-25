install:
	python setup.py develop --upgrade
test:
	cd example/basic_project && python manage.py test gcm
