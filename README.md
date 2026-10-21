# Overview

This is is a discord bot designed to be locally run alongside or a device that can reach an Azuracast instance.  Upon deploying to the server, the bot is able to join into a vc alongside a listener and broadcast your audio for the entire channel.  Listeners are also able to see metadata regarding the currently playing track (Title, artist, album art) and request additional tracks similarly to the official player included in azuracast 

# Requirements 

 - [Python >= 3.8](https://www.python.org/)
 - [FFmpeg](https://www.ffmpeg.org/)
 - Access to the Azuracast Mount Point
 - (Optional) The Azuracast station API key

# Installation 
 - Clone the repo
 - Open the folder in a terminal
 - (**OPTIONAL BUT RECOMMENDED**) Create a python virtual environment by running `python -m venv .venv`. The command to activate your virtual environment is specific to your operating system but you can find it easily online!
 - Install the PIP libraries using `Pip install -r requirements.txt`
 - Copy the `.env.example` and rename it too `.env` 
 - Add your stations information and discord token to the newly created `.env` file
 - Run the bot with `python __main__.py` 


 # Discord Commands
 - join (No args) 
	 - This command immediately joins the VC of the person who invoked it.
	 - If another person had summoned the bot to another channel that it is in currently it will pull it from that channel (Inter-server, not globally of course)
 - disconnect (No Args) 
	 - Instantly disconnects the bot from any VC in the server.
 - currentsong (No Args)
	 - Fetches information about the currently playing track and displays it in an embed
 - upnext (No Args) 
	 - Fetches information about the song thats about to come up and displays it in an embed 
 - request (SongName) 
	 - Requests a song by name from the azuracasts playlist. Does not have to be the currently running playlist, but only one with the option to accept requests turned on. 
 - queue 
	 - Displays the queue up to 5 songs (The max Azuracast has scheduled at a time)  in a bulleted list format.

 

