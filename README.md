# Psychopomp
A simple Discord bot handling voting for a game. 

Players vote for each other using either a server channel or by directly contacting your bot. On every vote change the bot publishes the current standing of the votes in a given text channel. 

To activate the vote, you @-mention another user in any text channel with the activating expression from the .env file. 

| Commands | Effect | 
| --- | --- |
|!status| Gives a small overview of the state of the game: timer (if any), voting if enable and current standing | 
|!settings| List the current settings | 
|!settings set \<parameter\> \<value\> | Change a setting, for example, '!settings set voting_channel pantheon'. Note that if you want to set a value that has a space in it you need to surround it with double quotes |
|!timer \<minutes\>| Starts a timer for X minutes. If there was a timer, it will be replaced by the new one. | 
|!timer pause| Pause the current timer |
|!timer continue| ...and continue the current timer. No effect if there is no timer or if it is still running | 
|!votes clean| Remove all the current votes | 
|!votes standing| Publishes the current standing in the votes channel |  
|!votes show | Shows you an overview of how everyone voted  | 
|!votes open | Enable voting. By default, voting is _disabled_ | 
|!votes close | Disable voting |

These commands are only useable by server admins. I suggest creating a seperate channel where you can cozy down with the bot. 

An example game round:
- In the zero state, the timer is disabled and voting is not allowed. You take the time to explain players how the game works. 
- Using the "!timer 10" command you set a timer for 10 minutes. Voting is now allowed.
- The timer will call out how much time is left 
- When the timer reaches 0, voting is once again disabled



