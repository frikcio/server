# Django boards
____
Small instruction to start this project on your machine:

##	What you need:
To start project your machine must have docker
____
###	To start the project:

setup:

Open directory with `docker-compose.yml` and `.env.example` file 

copy `.env.example` as `.env` and enter value

Open terminal/consol/CLI and write commands:

###	Commands:

run this command for create tables in database:
 
```
	docker-compose run server python manage.py migrate
```

for create superuser:

```
	docker-compose run server python manage.py createsuperuser
```

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

if project runs in the background, to stop project:
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
