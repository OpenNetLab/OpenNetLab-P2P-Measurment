docker_image := net-env
docker_file := dockers/Dockerfile

all: net-env

net-env:
	docker pull ubuntu:20.04
	docker build . --build-arg UID=$(shell id -u) --build-arg GUID=$(shell id -g) -f $(docker_file) -t ${docker_image}

