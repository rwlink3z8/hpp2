build:
		docker build --force-rm $(options) -t flask-site-100:latest

build-prod:
		$(MAKE) build options="--target production"

compose-start:
		docker-compose up --remove-orphans $(options)

compose-stop:
		docker-compose down --remove-orphans $(options)

compose-app-py:
		docker-compose run --rm $(options) website python app.py $(cmd)
