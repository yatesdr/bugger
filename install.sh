
sudo docker stop bugger-app
sudo docker container rm bugger-app

# Build the docker image
./build.sh

# Install and restart=always
sudo docker run \
 --device /dev/vchiq:/dev/vchiq \
 -p 80:8001 \
 --mount type=bind,src="$(pwd)/svg",target="/svg" \
 --restart always \
 --name "bugger-app" \
 -d \
 bugger

