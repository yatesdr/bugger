FROM dtcooper/raspberrypi-os:python3.11 
#RUN apk --no-cache add msttcorefonts-installer fontconfig && \
#    update-ms-fonts && \
#    fc-cache -f


#RUN apk add --no-cache build-base cairo-dev cairo cairo-tools jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN python3 -mpip install pip
RUN pip3 install uvicorn 
RUN pip3 install fastapi 
RUN pip3 install cairosvg 
RUN pip3 install numpy
RUN pip3 install dispmanx

#RUN apk add --no-cache libraspberrypi0

COPY . /app


WORKDIR /app
ENTRYPOINT ["python3","app.py"]
