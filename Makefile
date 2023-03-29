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

##########
# Server #
##########

.PHONY: s-server
s-server:
	docker-compose run --rm -p 2001:5000 -w /code python-picar python server.py

.PHONY: s-commander
s-commander:
	docker-compose run --rm -w /code python-picar celery -A commands worker --concurrency=1 -l INFO
