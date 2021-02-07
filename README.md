[![LightWeight](https://img.shields.io/badge/_-YEAH_BUDDY!-brightgreen)]()
[![LightWeight](https://img.shields.io/badge/_-Light_Weight,_baby!-brightgreen)]()
[![LightWeight](https://img.shields.io/badge/_-yep!_yep!_yep!_yep!_-brightgreen)]()


![Ronnie](./Resources/MD/Ronnie.jpg)

# RonnieBot (Discord Bot)

> RonnieBot is a **LIGHTWEIGHT** Discord Bot built with python and discord.py & uses Command Handler from [discord.py Guide](https://discordpy.readthedocs.io/en/latest/api.html)

## 🚀 Getting Started

```
git clone https://github.com/Tada0/RonnieBot.git
cd RonnieBot
pip install -r -requirements.txt
```

Make sure to also install [FFMPEG](https://ffmpeg.org/download.html) 

After installation finishes you can use `cd src; python3 client.py` to start the bot.

## ⚙ Configuration

⚠ **Note: Never commit or share your token or api keys publicly** ⚠

Fill the .env file with information

```shell script
TOKEN=""
DB_PATH=""
SOUNDS_PATH=""
DEFAULT_INTERVAL=""
DEFAULT_QUOTE_TIME=""
```

Default values:

```shell script
DB_PATH="../Resources/DB/db.json"
SOUNDS_PATH="../Resources/Sounds"
DEFAULT_INTERVAL=300
DEFAULT_QUOTE_TIME=22:00
```

## 📝 Features & Commands

> Note: Supported prefixes are '!', '?' and '#'
>
> In order to use RonnieBot you need to be connected to a Discord Voice Channel

* See help

`!ronnie`

* Add RonnieBot to Discord Voice Channel

`!ronnie_add`

* Remove RonnieBot from Discord Voice Channel

`!ronnie_remove`

* Set interval between RonnieBot playing Ronnie sounds (seconds)

`!ronnie_interval <INTEGER>`

* Set time when RonnieBot will send an inspirational quote to the Text Channel

`!ronnie_quote_time <HH:MM>`

* Post inspirational quote

`!ronnie_quote`

* Play randomly chosen Ronnie sound

`!ronnie_sound`

* **VIBE CHECK**

`!ronnie_vibe_check`


## 🤝 Contributing

1. [Fork the repository](https://github.com/Tada0/RonnieBot/fork)
2. Clone your fork: `git clone https://github.com/<YOUR_USERNAME>/RonnieBot.git`
3. Create your feature branch: `git checkout -b my-new-feature`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request
