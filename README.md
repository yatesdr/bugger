# Bugger
Bugger takes an SVG template and renders it on the HDMI output of a Raspberry-Pi4.   This is useful for real-time overlays such as scoreboards, lower thirds, or other vector graphics.   It exposes a simple POST interface for basic template substitution and file selection.

## How to use it
Get your raspberry pi 4 and install Raspbian-64 bit minimal.   Install docker, then clone the repo and run ./install.sh.   You'll have to design your SVG lower thirds or other graphics, a few tests are included and with time I'll add more examples.

## How to integrate it
I use this to generate a downstream key for use with Atem series switchers, using Companion and a Streamdeck.   Basically, the Companion does a post request to the raspberry pi to load the title, then switches the downstream key to whatever input the pi is hooked to.   The connection between your switcher and the pi is via HDMI, or SDI if you use a converter.

## How to make it do something
Once the docker image is installed, it will run and take over the display.   You'll see a blank display, and port 80 will be available for the API.   You need to upload your SVG overlay files to ~/bugger/svg, and pass in a command to render them.
```
scp my_file.svg user@<pi_ip_address>:/home/pi/bugger/svg/
```


## Example API post from Python
Here we have prepared a corporate lower third we want to use, and the template has $NAME, $TITLE, and $TOPIC.   We call the file, pass the chromakey color we want (0,255,0) = Green, and pass in the substitutions we want to make in the file.   Now we will see the display update with a green pre-multiplied key behind the transparent parts of the SVG.

Example usage from API:
```
import requests
url = "http://192.168.35.32:80/"

data = {
        "fname": "/svg/my_svg_filesvg",
        "subs": [
            ("$NAME","Your Name"),
            ("$TITLE","Your Title, Your Business"),
            ("$TOPIC", "Introduction")
            ],
        "chromakey": (0,255,0)
}

x = requests.post(url,json=data)
```


## Why does this exist?
I wanted an easy way to get dynamic titles into my switcher.   You can do similar overlays in OBS or other software based solutions, but sometimes hardware is just easier to use.   The goal was to integrate a streamdeck into the atem for switching titles through dozens of presenters throughout the day, and it does that well and with lots of flexibility.


## TODO 
This was hacked together in a couple hours, so the code is pretty ugly and there's no error checking.  It works fine but if you pass in bad requests it does not recover gracefully.  If this happens the screen will go back to raspberry pi console, and you'll have to restart the docker app ```sudo docker restart bugger-app```.   The display runs in a separate thread so uvicorn continues running happily, need to fix this. 
