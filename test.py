from random import uniform
import time, io, cairosvg, numpy 
from dispmanx import DispmanX
from PIL import Image

def svg2np(filename,resolution=(1920,1080)):
   mem = io.BytesIO()
   cairosvg.svg2png(url=filename, write_to=mem, output_width=resolution[0], output_height=resolution[1])
   npa = numpy.array(Image.open(mem))

   # Pre-multiply the alpha as green (0,255,0) and eliminate it.
   # This has the effect of mixing with a green underlayment for chroma-keying.

   npa[:,:,0]=  ( ( (npa[:,:,0]/255) * (npa[:,:,3]/255) ) ) * 255  # Red
   npa[:,:,1]=  ( ( (npa[:,:,1]/255) * (npa[:,:,3]/255) ) + ((1-npa[:,:,3]/255)))*255 # Green, mixed with (0,255,0) background.
   npa[:,:,2]=  ( ( (npa[:,:,2]/255) * (npa[:,:,3]/255) ) ) * 255 # Blue

   #If alpha is included, strip it out (will be black)
   npa = npa[:,:,:3] 

   return npa #numpy.array(Image.open(mem))

# The display will use chroma keying, so RGB is ideal.
display = DispmanX(pixel_format="RGB", buffer_type="numpy")
width, height = display.size

print("Display opened:  (width, height): ", width, height)

# Read SVG file into Numpy array
res = svg2np('/home/derek/bugger/svg/scoreboard4.svg', resolution=(1920,1080))
print("Image loaded, shape: ", res.shape)
numpy.copyto(display.buffer,res)
display.update()

time.sleep(5)

