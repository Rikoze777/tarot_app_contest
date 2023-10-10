# Deployment with Docker

- Docker and docker-compose must be installed.
- Make sure that `.env` and `requirements.txt` are present in the `backend` folder, then run the command
```bash
docker-compose up --build
```

- To create a superuser, run the command, where container_name is the name of your container:
```bash
docker exec -it container_name python manage.py createsuperuser
```