# Psychopomp
A simple Discord bot handling voting for a game. 

Players vote for each other using either a server channel or by directly contacting your bot. On every vote change the bot publishes the current standing of the votes in a given text channel. 

To activate the vote, you call out a vote to @-mention any user in any text channel, or message the bot directly effectively hiding your vote for the other players. 

The bot publishes standing changes to a preconfigured channel. It also has a timer, publishing to the same channel.     

 ### Player commands
 
| Commands | Effect | 
| --- | --- |
| 'stem' | Using the expression as configured in the .env, the player can vote for other players using the @ notation. If in a private message, the bot will try to find the mentioned player and if not found, offer a menu where you can use number based vote selection. | 
| 'verwijder'..'stem' | The last vote this player gave is removed and standings are updated | 


 ### Server Admin commands
| Commands | Effect | 
| --- | --- |
|!status| Gives a small overview of the state of the game: timer (if any) and minutes left and weither voting is enabled. By default, voting is closed until a timer starts | 
|!settings| List the current settings | 
|!settings set \<parameter\> \<value\> | Change a setting, for example, '!settings set voting_channel pantheon'. Note that if you want to set a value that has a space in it you need to surround it with double quotes |
|!timer \<minutes\>| Starts a timer for X minutes. If there was a timer, it will be replaced by the new one. This opens voting. If the timer ends, voting is closed. | 
|!timer pause| Pause the current timer |
|!timer continue| ...and continue the current timer. No effect if there is no timer or if it is still running | 
|!votes clean| Remove all the current votes | 
|!votes standing| Publishes the current standing in the votes channel |  
|!votes show | Shows you an overview of how everyone voted  | 
|!votes open | Enable voting. By default, voting is _disabled_ | 
|!votes close | Disable voting |
|!intro list | Show all MP3 files | 
|!intro play <mp3 file name or number> | Play an MP3 on the preconfigured voice channel. Can overwrite an existing play |
|!intro pause | Pause playing an MP3 |
|!intro resume | Resume playing a paused MP3 |
|!helpme | Show these options, but in discord |  


These commands are only useable by server admins. I suggest creating a separate channel where you can cozy down with the bot. 

## Gameplay
An example game round:
- In the zero state, the timer is disabled and voting is not allowed. You take the time to explain players how the game works. 
- Using the "!timer 10" command you set a timer for 10 minutes. Voting is now allowed.
- The timer will call out how much time is left 
- Players call out votes in text channels. Alice votes for Bob, Bob votes for Bob, Charles votes for Aliex.   
- When the timer reaches 0, voting is once again disabled. A final standing is published showing Bob has 2 votes and Alice has 1 (but not who voted for them) 


## Installation
- Install the requirements (pip install -r requirements.txt)

- Copy the example .env.example to .env and change the parameters
  - Find the token by opening https://discord.com/developers/, adding a new application, opening the Bot menu and generating a token (below the username). 
  - Authorize the bot by opening the "URL Generator" in the OAuth2 menu, dashing application.commands, Bot and Administrator and opening the redirect URL. Select your discord server there. 
- Put the FFMPEG executeable in a location and change the parameter in the .env file
- Put some MP3s in the MP3 directory  
- Start the psychopomp.py python script (or use the systemd file)

## Example systemd file
```json
[Unit]
Description=Psychopomp discord bot

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/psychopomp/psychopomp.py
WorkingDirectory=/usr/local/bin/psychopomp
Restart=on-failure
RestartSec=5s 
StandardOutput=append:/var/log/psychopomp.log
StandardError=append:/var/log/psychopomp.log
```

## Adding a locale
This bot uses the Python gettext library. To regenerate the .pot file: 
```
python.exe 'C:\Program Files\Python38\Tools\i18n\pygettext.py' -n -d psychopomp .\lib .\psychopomp.py
python 'C:\Program Files\Python38\Tools\i18n\msgfmt.py' -o .\locales\nl_NL\LC_MESSAGES\psychopomp.mo .\locales\nl_NL\LC_MESSAGES\psychopomp

```
