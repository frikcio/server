# Django boards
____
Small instruction for Ubuntu, to start project on your machine:
##What you need: 
1a) Check availability of docker on machine:
```
docker --version
```
1b) If docker not intalled on your machine, download docker:
	###Step 1: Updating the Local Repository

	Open a terminal window and update the local repository with:
	```console
	sudo apt update
	```
	###Step 2: Installing Docker
	```console
	sudo apt install docker.io
	```
	###Step 3: Checking Docker Installation
```console
	docker --version
```
	###Step 4: Starting Docker Service 
```console
	sudo systemctl start docker
```
	Then, enable it to run at startup:
```console
	sudo systemctl enable docker
```
	To check the status of the service, run:
```console
	sudo systemctl status docker
```
2) 
setup:
```
docker-compose up
```
