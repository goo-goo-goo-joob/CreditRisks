DOCKER_REGISTRY = hub.asciishell.ru
DOCKER_IMAGE = $(DOCKER_REGISTRY)/creditrisks
APP_NAME ?= app

ifeq ($(TRAVIS_BRANCH), master)
	DOCKER_TAG = latest
else
	ifdef TRAVIS_TAG
		DOCKER_TAG = $(TRAVIS_TAG)
	endif
endif

all:
	$(info $$DOCKER_REGISTRY is [$(DOCKER_REGISTRY)])
	$(info $$DOCKER_IMAGE is [${DOCKER_IMAGE}])
	$(info $$APP_NAME is [$(APP_NAME)])
	$(info $$DOCKER_TAG is [$(DOCKER_TAG)])

.PHONY: docker-push
docker-push:
	docker tag $(APP_NAME) $(DOCKER_IMAGE)/$(APP_NAME):$(DOCKER_TAG)
	docker push $(DOCKER_IMAGE)/$(APP_NAME):$(DOCKER_TAG)
.PHONY: docker-deploy
docker-deploy:
	docker login $(DOCKER_REGISTRY) --username $(USERNAME) -p $(TOKEN)
	make docker-push
	docker logout

.PHONY: docker-deploy-ci
docker-deploy-ci:
	if [ "$(DOCKER_TAG)" != "" ]; then \
		make docker-deploy; \
	fi