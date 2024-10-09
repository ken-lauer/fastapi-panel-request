BUILDKIT_PROGRESS=plain
SERVER_PORT=8882
ROOT_PATH?=/

export BUILDKIT_PROGRESS

build:
	docker build -t panel-docker:latest .

run:
	docker run --publish 8882:8080 --env-file .env -it panel-docker:latest

dev:
	fastapi dev --port 8882 src/main.py --root-path $(ROOT_PATH)


.PHONY: build run dev
