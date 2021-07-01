# Django boards
____
Small instruction for Ubuntu, to start project on your machine:

##	What you need:
 
###	1a) Check availability of docker on your machine:
```
	docker --version
```
###	1b) If docker not intalled on your machine, download docker:
####	Step 1: Updating the Local Repository

Open a terminal window and update the local repository with:

```
	sudo apt update
```

####	Step 2: Installing Docker

```
	sudo apt install docker.io
```

####	Step 3: Checking Docker Installation

```
	docker --version
```

####	Step 4: Starting Docker Service 

```
	sudo systemctl start docker
```

Then, enable it to run at startup:

```
	sudo systemctl enable docker
```

To check the status of the service, run:

```
	sudo systemctl status docker
```
###	2) Enter these commands to start the project
setup:
```
	docker-compose up
```
Maybe that's all)
