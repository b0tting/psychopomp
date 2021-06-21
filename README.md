# Psychopomp
A simple Discord bot handling voting for a game. 

Players vote for each other using either a server channel or by directly contacting your bot. On every vote change the bot publishes the current standing of the votes in a given text channel. 

To activate the vote, you @-mention another user in any text channel with the activating expression from the .env file. 


# TODO:
- Countdown starten
- Tussenstand melden bij tijdstippen
- Melding bij einde countdown
- admin commandos: leegmaken, stoppen, starten, eindstand


| Commands | Effect | 
| --- | --- |
|!status| Gives a small overview of the state of the game: timer (if any), voting if enable and current standing | 
|!setting| List the current settings | 
|!timer <minuten>| Starts a timer for X minutes. If there was a timer, it will be replaced by the new one. | 
|!timer pause| Pause the current timer |
|!timer continue| ...and continue the current timer. No effect if there is no timer or if it is still running | 
|!votes clean| Remove all the current votes | 
|!votes standing| Shows the current standing in the votes channel |  
|!votes show | Shows you the current votes in the channel you send messsage | 
|!votes start| Enable voting. By default, voting is _disabled_ | 
|!votes stop| Disable voting |
 
