# DataCollector
A Simple Java Backend to Store User Requests

## Introduction
This sub-project is supposed to be deployed in a EC2 instance to collect testing results from testing instances.

## Prerequisites
1. OpenJDK 17
2. Maven
3. Docker

## How to use
1. Clone this repository to your local machine
2. Build the project with Maven
~~~ zsh
mvn clean package
~~~
3. Build the docker image
~~~ zsh
docker build -t data-collector/app .
~~~
4. Run the docker image
~~~ zsh
docker run -p 8080:8080 data-collector/app
~~~
5. Tag the docker image and push it to your docker hub. (Optional)
~~~ zsh
docker tag data-collector/app:latest <your_docker_hub_username>/data-collector:app
docker push <your_docker_hub_username>/data-collector:app
~~~
6. Existing docker image is available at `docker pull yihongjin/data-collector:app`
