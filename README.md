# timer  
### by KsmBl / Whisper  

## installation:  
clone the github repository to your local device with  
`git clone https://github.com/KsmBl/timer/`  
  
Remove all unusefull stuff like README.md or the alarm.mp3, when you wanna use your own audio file.  
Make the main.py runable with  
`cd timer && chmod +x ./main.py`  

Edit the audio path in the main.py file  
`vim ./main.py`  
Write in line 8 the path to your audio file.  
  
Move the main.py to a location where youre fine with it. Like in ~/.bin/.  
Then create a symlink to /bin/ with  
`sudo ln -s /path/to/your/bins/timer/main.py /bin/timer`  
  
Now timer should be runable in your terminal aslong /bin/ is in your $PATH. But thats default for near to every Linux distro.  
  
## usage:  
### new:  
Create a new timer named pizza which needs 15 Minutes:  
`timer new pizza 15:00`  
  
Alternative:  
`timer new pizza 900`  
  
Create a new timer which needs very long:  
`timer new cake 1:00:00`  
this timer needs one hour.  
  
### list:  
List all active timers:  
`timer list`  
  
### pause:  
Pause a timer named pizza:  
`timer pause pizza`  
  
### continue:  
Continue a paused timer named pizza:  
`timer continue pizza`  
  
### delete:  
To delete an active timer named pizza:  
`timer stop pizza`  
  
### view:  
To see how long your pizza still need just type:  
`timer view pizza`  
