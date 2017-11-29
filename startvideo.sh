#export LD_LIBRARY_PATH=/home/pi/Projects/mjpg-streamer/mjpg-streamer-experimental &
/usr/local/bin/mjpg_streamer -o "output_http.so -w $LD_LIBRARY_PATH/www" -i "input_raspicam.so -x 400 -y 300 -fps 10 -rot 270 -quality 25" &> /home/pi/stream.log &

