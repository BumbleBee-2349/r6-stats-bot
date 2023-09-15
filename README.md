# R6 Stats Bot

**r6-stats-bot** is a Python Discord bot that collects Rainbow Six Siege player stats.

## Getting Started

To run the bot, make sure you have Python3+ installed. You can set up the project by following these steps:

1. Clone the project to your repository and if you want to run locally
```
$ cd r6-stats-bot
```

```
$ pip install -r requirements.txt
```

2. You should create a `.env` file with a `DISCORD_TOKEN=TOKEN` to run the bot

3. Run the bot:
```
$ python3 main.py
```

4. You can run on a docker container as well, so build the image:
```
$ docker build --tag r6-bot .
```
5. Run the bot on a docker container:
```
$ docker run --name r6-bot -d r6-bot
```

## How it looks
![Alt text](https://raw.githubusercontent.com/matheusnicolas/readme-images/master/Screenshot%202023-08-15%20at%2010.26.53.png)