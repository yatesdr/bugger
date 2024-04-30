# Bugger
Bugger takes an SVG template and renders it on the HDMI output of a Raspberry-Pi4.   This is useful for real-time overlays such as scoreboards, lower thirds, or other vector graphics.   It exposes a simple POST interface for basic template substitution and file selection.

## How to use it
Get your raspberry pi 4 and install Raspbian-64 bit minimal.   Install docker, then clone the repo and run ./install.sh.   You'll have to design your SVG lower thirds or other graphics, a few tests are included and with time I'll add more examples.

## Raspberry Pi isn't working with my Display / HDMI switcher / SDI converters!
Yes, this is a known issue with Raspberry Pi's, they like to do weird things with their HDMI ports if you don't have a normal monitor connected.

You can usually fix it by editing /boot/firmware/config.txt and setting the following options for 1080p output:
/boot/firmware/config.txt:
```
hdmi_ignore_edid=0xa5000080
display_autodetect=0
hdmi_force_hotplug=1
hdmi_group=1
hdmi_mode=34
```

The install script will do it for you, but make sure you're using the "Fake" vt4-kms driver:
```
dtoverlay=vc4-fkms-v3d
```

Additionally, if the above fixes aren't working for your converters you can try adding this to the end of your kernel commandline in /boot/firmware/cmdline.txt:
```
video=HDMI-A-1:1920x1080Die@60
```

These changes get it working with the BlackMagic bi-directional converters I use.



## How to integrate it
I use this to generate a downstream key for use with Atem series switchers, using Streamdeck and Bitfocus Companion.   

Basically, you program a button on the Streamdeck to trigger Companion's HTTP post module, which sends a post request to the raspberry pi to load the desired title and template substitutions.   If you wish, you can also add an action to switch the downstream key to whatever input the pi is hooked to.   The connection between your switcher and the pi is via HDMI, or SDI if you use a converter, so the setup is pretty simple.

## How to make it do something
Once the docker image is installed, it will run and take over the Raspberry Pi's main output display.   You'll see a black screen by default, and port 80 will be available for the API to receive requests on.   You need to upload your SVG overlay files to ~/bugger/svg, and pass in a request to open and render them.
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
        "fname": "/svg/my_svg_file.svg",
        "subs": [
            ("$NAME","Your Name"),
            ("$TITLE","Your Title, Your Business"),
            ("$TOPIC", "Introduction")
            ],
        "chromakey": (0,255,0)
}

x = requests.post(url,json=data)
```

## Using with Bitfocus Companion
You need to add the generic http driver, and POST the data in valid json.  Note that the svg directory is mapped inside the docker container at /svg/, and if you push live updates to that folder they'll appear without restarting anything.

Example POST - Needs files, and template variables to work.
```
{
  "fname": "/svg/Lower_Third.svg",
  "chromakey": [0,255,0],
  "subs": [["$NAME","Your Name"]]
}
```

## Why does this exist?
I wanted an easy way to get dynamic titles into my switcher.   You can do similar overlays in OBS or other software based solutions, but sometimes hardware is just easier to use.   The goal was to integrate a streamdeck into the atem for switching titles through dozens of presenters throughout the day, and it does that well and with lots of flexibility.

The beauty of this method is that it can fully render the SVG document as a template.   So if you want to change colors or title strings this is perfectly possible depending how you construct your SVG.   For example, to render a Baseball scoreboard you can keep score in a separate application and then fill in "ball1" as red if there's more than one ball.   You can fully automate this with streamdeck variables to create your post request substitutions if you'd like. 


## TODO 
This was hacked together in a couple hours, so the code is pretty ugly and there's no error checking.  It works fine but if you pass in bad requests it does not recover gracefully.  If this happens the screen will go back to raspberry pi console, and you'll have to restart the docker app ```sudo docker restart bugger-app```.   The display runs in a separate thread so uvicorn continues running happily, need to fix this. 
