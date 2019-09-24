DOCKER_REGISTRY = docker.pkg.github.com
DOCKER_IMAGE = $(DOCKER_REGISTRY)/goo-goo-goo-joob/creditrisks
APP_NAME = app

.PHONY: docker-deploy
docker-deploy:
    docker login $(DOCKER_NAME) --username $(USERNAME) -p $(TOKEN)
    docker tag app $(DOCKER_IMAGE)/$(APP_NAME):$(TRAVIS_BRANCH)
    docker push $(DOCKER_IMAGE)/$(APP_NAME):$(TRAVIS_BRANCH)
    docker logout
