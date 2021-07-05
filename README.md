# Django boards
____
Small instruction to start this project on your machine:

##	What you need:
 
###	1) Check availability of docker on your machine:

```
	docker --version
```
If docker not installed on your machine:

Linux:
https://docs.docker.com/engine/install/#server

macOS:
https://docs.docker.com/docker-for-mac/install/

Windows 10:
https://docs.docker.com/docker-for-windows/install/
____
###	2) If you have docker on your machine, to start the project:

setup:

a) open directory with `docker-compose.yml` and `.env.example` file 

rename `.env.example` to `.env` and enter value for (SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, SERVER_PORT) 

b) open terminal/consol/CLI

###	Commands:

to build project and run:

```
	docker-compose up --build
```

to build project and run in the background:
```
	docker-compose up --build -d
```

to run the built project:
```
	docker-compose start
```

to stop project:
```
	docker-compose stop 
```

to disassemble project:
```
	docker-compose down
```

to disassemble project and delete database:
```
	docker-compose down --volume
```
____
Maybe that's all)
