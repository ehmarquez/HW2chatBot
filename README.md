# HW2chatBot : Created by Charles Marquez (Aykon)

A Halo Wars 2 Discord Bot that provides and visualizes data from the Halo Wars 2 API. Currently a work in progress. Lots more functions and additional functionality to be added.

## Prerequisites
```
pip install numpy
pip install matplotlib
pip install pylab
pip install time
```

#### discord.py version 1.0.0a is necessary.
```
pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
```
May cause issues with previously install Discord library (0.16.12 and earlier)

## Requirements

After signing up for Halo Wars 2 API key and creating 
your own Discord bot with its own authentication key.

Create a file.
```
keys.py 
```
Functions Included:
```
hw2key()
discordkey()
```
Refer to 
```
keysample.py
```
Replace the corresponding 'xxx' values with your Halo Wars 2 API key and your Discord bot token.

### How to Run
```
python wowBOT2.py
```

The bot should log on to any servers you've assigned it to.

#### Commands

Currently Active:
```
/matchRates {matchId}
/matchBuild {matchId} {playerName}
/mmr {playerName}
```

Work in Progress:
```
/deathMap {matchId}
/unitDeaths {matchId} {playerName}
```

