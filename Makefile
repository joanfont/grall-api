.PHONY: build
build:
	docker compose build app

.PHONY: push
push:
	docker compose push app

.PHONY:	up
up:
	docker compose up -d app