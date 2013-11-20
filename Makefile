install:
	python setup.py develop --upgrade
test:
	cd example && python manage.py test gcm
