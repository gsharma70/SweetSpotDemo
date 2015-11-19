# SweetSpotDemo
Occupant Aware Environment Demo

This is a simple demonstration of creating of occupant aware environments.

ws_server.js is the server code that basically implements a handshake with the clients and
echoes everythin that is sent to it. You need to install nodejs in order to run this server.

circles_v1.py is an implementation of the occupant aware environment. It reads in images from
a live camera stream and process the live images to extract certain regions in order to determine
whether a person is there or not in those regions. OpenCV and python is required to run this code.

index.html is an implementation of the client side where the results of the human aware environment
can be seen. It receives binary results from the server and based on where the user is in the room, plays 
or pauses the videos. Google's speech recognition API is also incorporated in this so that when a person
is in a sweet spot, whatever he/she speaks is transcribed onto the video.
