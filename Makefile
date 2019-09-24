DOCKER_REGISTRY = docker.pkg.github.com
DOCKER_IMAGE = $(DOCKER_REGISTRY)/goo-goo-goo-joob/creditrisks
APP_NAME = app

all:
	$(info $$DOCKER_REGISTRY is [$(DOCKER_REGISTRY)])
	$(info $$DOCKER_IMAGE is [${DOCKER_IMAGE}])
	$(info $$APP_NAME is [$(APP_NAME)])

.PHONY: docker-deploy
docker-deploy:
	docker login $(DOCKER_REGISTRY) --username $(USERNAME) -p $(TOKEN)
	docker tag app $(DOCKER_IMAGE)/$(APP_NAME):$(TRAVIS_BRANCH)
	docker push $(DOCKER_IMAGE)/$(APP_NAME):$(TRAVIS_BRANCH)
	docker logout
