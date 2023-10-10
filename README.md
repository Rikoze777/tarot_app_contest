# Tarot bot

[tarot-bot](https://t.me/tarot_contest_bot) - a mini-application that provides a demo process for receiving tarot readings. The user is given the opportunity to purchase a subscription with which he can choose all types of tarot readings.

## Deploy with Docker

If you want to deploy it easy with Docker. [Read](docker.md) this. 

## Installing

- Deploy a virtual environment
- Install libraries:
```bash
cd backend/ && pip install -r requiremenets.txt
```
- Create a `.env` file with the following variables in `backend` folder:
    1. BOT_API_TOKEN='Your bot token'
    2. ALLOWED_HOSTS='Your hosts'
    3. SECRET_KEY='Django secret key'
    4. DEBUG='True for dev and False for prod'
    5. PROVIDER_TOKEN='provider token from [BotFather](https://t.me/BotFather)'

- Perform migrations
```bash
cd backend/ && python3 manage.py migrate
```

- [Deploy fronted](frontend/README.md)

- Run Django:
```bash
cd backend/ && python3 manage.py runserver
```
- Run bot in another terminal:
```bash
cd backend/bot/ && python3 bot.py
```