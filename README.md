# Bugger
Bugger takes an SVG template and renders it on the HDMI output of a Raspberry-Pi4.   This is useful for real-time overlays such as scoreboards, lower thirds, or other vector graphics.   It exposes a simple POST interface for basic template substitution and file selection.

## How to use it
Get your raspberry pi 4 and install Raspbian-64 bit minimal.   Install docker, then clone the repo and run ./install.sh.   You'll have to design your SVG lower thirds or other graphics, a few tests are included and with time I'll add more examples.


## How to integrate it
I use this to generate a downstream key for use with Atem series switchers, using Streamdeck and Bitfocus Companion.   

Basically, you program a button on the Streamdeck to trigger Companion's HTTP post module, which sends a post request to the raspberry pi to load the desired title and template substitutions.   If you wish, you can also add an action to switch the downstream key to whatever input the pi is hooked to.   The connection between your switcher and the pi is via HDMI, or SDI if you use a converter, so the setup is pretty simple.

## How to make it do something
Once the docker image is installed, it will run and take over the Raspberry Pi's main output display.   You'll see a black screen by default, and port 80 will be available for the API to receive requests on.   You need to upload your SVG overlay files to ~/bugger/svg, and pass in a request to open and render them.
```
scp my_file.svg user@<pi_ip_address>:/home/pi/bugger/svg/
```

If you're plugged directly into a normal monitor or TV when you boot the pi, this should work as-is.   If you're using an SDI converter or some type of HDMI switcher, you will probably need to set additional options to force display conformance and output modes (see Troubleshooting at the end of this document).   Once you find the right options, this is tested to work with Atem mini, BM bidirectional converters, and BM HDMI to SDI converters, as well as the other Atem Switchers that use 1080p60 or 1080p30.


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


# Troubleshooting Display Issues

## Raspberry Pi4b isn't working with my Display / HDMI switcher / SDI converters!

Yes, this is a known issue with Raspberry Pi's, they like to do weird things with their HDMI ports if you don't have a normal monitor connected, but fortunately you can force them to use the desired configurations. 

1)  Make sure you didn't install X server, this application is meant to run on the base "Lite" Raspbian distribution.

2)  Fix display issues by forcing the resolutions you want.  You can usually fix it by editing /boot/firmware/config.txt and setting the following options for 1080p output:

/boot/firmware/config.txt:
```
hdmi_ignore_edid=0xa5000080
display_autodetect=0
hdmi_force_hotplug=1
hdmi_group=1
hdmi_mode=34   # 1080p30.  Set hdmi_mode=16 for 1080p60, or hdmi_mode=46 for 1080i/120Hz depending on your switcher.
```


The install script will do it for you, but make sure you're using the "Fake" vt4-kms driver:
```
dtoverlay=vc4-fkms-v3d
```

Additionally, if the above fixes aren't working for your converters you can try adding this to the end of your kernel command line:

/boot/firmware/cmdline.txt:
```
video=HDMI-A-1:1920x1080Die@60
```
Select the video mode and framerate suitable for your switcher or converter.

The above changes get it working with the BlackMagic bi-directional 3G SDI / HDMI converters I use, which tend to be a bit touchier than most when it comes to conversion standards.


## I'm using an Atem M/E 1 (or other SDI switcher) and nothing is showing up.
These are touchy about the video standards, but do work.   Most of the time you'll need to log in to the settings page and select a compatible video mode for the switcher.   I have had luck with 1080p60 and 1080p30, but you may just have to play with it a bit to find the best solution.   The video mode of the switcher and the converter must match the video mode you force using the above options or it will probably not work, or will be glitchy.


## This isn't working on my Banana Pi, Raspberry PI 3, 400, etc.
This is only tested on the Raspberry Pi 4, and is tightly integrated to the hardware.   It may work on others, but no support or issues will be accepted.   Go buy a Pi 4 and put it in a case, load this up and move on.

## Template substitution isn't working
You'll probably need to at least hand-edit your SVG files to make sure all your strings are together.   Use VIM or Nano, and make sure it all makes sense and is somewhat human-readable.   Many of the SVG exports from photo software packages are pretty messy and split strings with <tspan ... > blocks, so the simple string substitution will be broken.

I use Affinity Photo to generate and export my SVG's, then hand edit them to make sure all the template variables are in the right place and intact.   They're often not.   If available, you should flatten transforms and not export non-compatible features.   In Affinity Photo, there are check-boxes for the conversions of how to handle these.

1)  Rasterize:  nothing
2)  Flatten Transforms
3)  Set ViewBox
4)  Add Line Breaks
5)  Use fonts that are web-compatible (TTF core fonts)

Even with all these set, a complicated layout is probably going to need hand editing to get the template variables into a suitable position.   I usually go through mine and make sure my $SUBSTITUTE strings are in-tact, and then manually place the text and apply styling to it.

## TODO 
This was hacked together in a couple hours, so the code is pretty ugly and there's no error checking.  It works fine but if you pass in bad requests it does not recover gracefully.  If this happens the screen will go back to raspberry pi console, and you'll have to restart the docker app ```sudo docker restart bugger-app```.   The display runs in a separate thread so uvicorn continues running happily, need to fix this. 

1)  Add a proper web interface for changing titles dynamically.    Right now I just use Bitfocus companion to send the POST request which works fine.
2)  Add error checking and handling
3)  Add monitoring and restart for crashed display thread.
