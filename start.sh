export LD_LIBRARY_PATH=/home/pi/Projects/mjpg-streamer/mjpg-streamer-experimental &
/opt/vc/bin/tvservice -o &
/usr/bin/sudo /usr/local/bin/python3.6 /home/pi/Projects/rc_sanic_server2.py &
/usr/local/bin/mjpg_streamer -o "output_http.so -w /home/pi/Projects/mjpg-streamer/mjpg-streamer-experimental/www" -i "input_raspicam.so -x 320 -y 240 fps 2 -rot 270 -quality 40 -ex auto -awb auto -vs"
