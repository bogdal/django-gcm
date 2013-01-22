install:
	python setup.py develop --upgrade
	pip install -r requirements.txt

test:
	cd example && python manage.py test gcm
