# Run without installing (for testing)
sudo docker run \
 --device /dev/vchiq:/dev/vchiq \
 -p 80:8001 \
 --mount type=bind,src="$(pwd)/svg",target="/svg" \
 bugger

