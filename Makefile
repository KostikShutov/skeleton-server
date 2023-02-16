##########
# Docker #
##########

.PHONY: d-up
d-up:
	docker-compose up -d

.PHONY: d-down
d-down:
	docker-compose down

.PHONY: d-restart
d-restart:
	docker-compose restart

.PHONY: d-python
d-python:
	docker-compose exec python-picar bash

#############
# Commander #
#############

.PHONY: s-commander
s-commander:
	docker-compose run --rm -w /code python-picar celery -A commands worker -l INFO
