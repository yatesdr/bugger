import time, io, cairosvg, numpy 
from dispmanx import DispmanX
from PIL import Image

class svg_display:

    chromakey=(0,255,0) # (R,G,B) in 8-bit color - Default is greenscreen
    target_resolution=(1920,1080) # (W,H) - Default is 1920x1080 / HD display
    display_resolution=None # Will be populated at init()
    display=None # Will be populated at init()

    def __init__(self):
        self.display, self.display_resolution  = self.get_display()

    # Loads an SVG from disk into a numpy array suitable for display with dismanx.
    # If the SVG contains an alpha channel, a chroma-key of the specified color is applied.
    def svg_load_with_chromakey(self, filename):

        mem = io.BytesIO()
        cairosvg.svg2png(url=filename, write_to=mem, output_width=self.target_resolution[0], output_height=self.target_resolution[1])
        npa = numpy.array(Image.open(mem))

        # If we have an alpha channel, apply the chroma key
        if (npa.shape[2]==4):
            npa[:,:,0]=  ( ( (npa[:,:,0]/255) * (npa[:,:,3]/255) ) + (self.chromakey[0]/255*(1-npa[:,:,3]/255)))*255 # Red
            npa[:,:,1]=  ( ( (npa[:,:,1]/255) * (npa[:,:,3]/255) ) + (self.chromakey[1]/255*(1-npa[:,:,3]/255)))*255 # Green
            npa[:,:,2]=  ( ( (npa[:,:,2]/255) * (npa[:,:,3]/255) ) + (self.chromakey[2]/255*(1-npa[:,:,3]/255)))*255 # Blue

        # Strip Alpha if exists, returns only RGB 
        return npa[:,:,:3] 

    # Class method to get a dispmanx display, in the RGB format.
    def get_display(self):
        display = DispmanX(pixel_format="RGB", buffer_type="numpy")
        width, height = display.size
        return display, (width, height)

    def set_chroma(self,k):
        self.chromakey=k

    # Main useful function, opens an SVG and renders it on the default display
    def show(self, filename):
        res = self.svg_load_with_chromakey(filename)
        numpy.copyto(self.display.buffer,res)
        self.display.update()


# Demonstration for testing
if __name__=="__main__":
    d = svg_display()
    d.chromakey=(255,0,0)
    d.show("scoreboard.svg")
    time.sleep(5)

