IMAGE ?= cicd-demo:local
CLUSTER ?= cicd

.PHONY: help test build run local-test cluster jenkins deploy-local status logs clean

help:
	@echo "make test         - run unit tests inside Docker"
	@echo "make build        - build the runtime image"
	@echo "make run          - run image on http://localhost:5000"
	@echo "make local-test   - test + build + probe container"
	@echo "make cluster      - create kind cluster + Jenkins (scripts/setup.sh)"
	@echo "make deploy-local - deploy local image to kind WITHOUT Jenkins"
	@echo "make status       - show pods/services"
	@echo "make clean        - tear everything down"

test:
	docker build --target test -t cicd-demo:test .

build:
	docker build --target runtime -t $(IMAGE) .

run: build
	docker run --rm -p 5000:5000 $(IMAGE)

local-test:
	./scripts/local-test.sh

cluster jenkins:
	./scripts/setup.sh

deploy-local: build
	kind load docker-image $(IMAGE) --name $(CLUSTER)
	kubectl apply -f k8s/namespace.yaml
	sed "s|DOCKER_IMAGE_PLACEHOLDER|$(IMAGE)|" k8s/deployment.yaml | kubectl apply -f -
	kubectl apply -f k8s/service.yaml
	kubectl -n cicd-demo rollout status deployment/cicd-demo --timeout=120s
	@echo "App: http://localhost:8081"

status:
	kubectl -n cicd-demo get pods,svc

logs:
	kubectl -n cicd-demo logs -l app=cicd-demo --tail=50

clean:
	./scripts/teardown.sh
