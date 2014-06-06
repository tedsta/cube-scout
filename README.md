# Cube Scout

This loyal trooper's got your back in the cubicle. He captures video from a device (such as a USB webcam), detects and recognizes faces, and informs every connected client of who he sees. No one can ever sneak up on you or your cubicle-mates again! There are more creative applications also, such as automatically switching windows when a boss is approaching.

Cube Scout is written in python and makes heavy use of OpenCV. It is tested with python2.7 and OpenCV 2.4.9.

# Dependencies

You'll need the python and OpenCV along with its python bindings installed to run the server. To run the client, all you need is python.

## Ubuntu

It's fairly simple to get Cube Scout running on an ubuntu machine.

If you only need to run the client, all you need to install is python:

`sudo apt-get install python`

To run the server, you'll also need OpenCV. [I found this tutorial that should help](http://www.sysads.co.uk/2014/05/install-opencv-2-4-9-ubuntu-14-04-13-10/):

Once you complete that, you're ready to run Cube Scout.

# Running

First, you'll need to download the code.

```
git clone https://github.com/tedsta/cube-scout.git
cd cube-scout
```

Then, to run the server:

`python cubescout.py <device_id>`

For example, on my Ubuntu desktop, I run it like this:

`./cubescout.py 0`

To run the client:

`python client_cube_scout.py <server_address>`

For example:

`./client_cube_scout.py localhost`
