# Flo-League Website
![](app\static\assets\logo.png?raw=True)
This repository contains the code for [FloLeague](https://www.flo-league.com), an elo based ranking website for the MMORPG Florensia.

## Stack
Flo-League uses [Flask](https://palletsprojects.com/p/flask/) as a framework. For the frontend, [Tailwindcss](https://tailwindcss.com/) is used.

## Matchmaking
Machtes are generated pseudo-randomly (at least those with team sizes >= 1). They will try to generate 'fair teams', which prevents multiple base classes to be in the same team, if it is avoidable.
Here is a rough plan on how this works (I'm bad at drawing and explaning, sorry!).
![](docs/matchmaking_algorithm.png?raw=True)


## Development
### Dependencies
If you want to run the project locally, you will have to install all needed dependencies.

Python: `pip install -r requirements.txt`

NodeJS: `npm install`

### .env file
You will need a .env file in the root directory with the following settings:
|Key|Description|
|--|--|
|FLASK_ENV|Either `development` or `production`.|
|SECRET_KEY|The secret key used by Flask.|

### Running
To run the webserver: `python main.py`

To re-build the css whenever a change is made, run the watcher by using `npm run watch:tailwind`.

You may have to populate the database with players first, to do so, run `python update_players.py`.

## License
[MIT License](https://opensource.org/licenses/MIT)
