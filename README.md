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

## Server

To run the server:

`python cubescout.py <device_id>`

For example, on my Ubuntu desktop, I run it like this:

`./cubescout.py 0 -s`

The '-s' option tells it to collect samples, which you can use to as training data. Samples are saved to the data/samples directory.

For each person you want to recognize, create a folder in 'data/images/' (no spaces in names). For example, my name is Teddy, so my face images are located in '<cube-scout-root>/images/teddy/'. Whenever you update the images, you need to run this command for the images to be used by cube scout:

`python create_csv.py data/images > data/faces.csv`

## Client

To run the client:

`python client_cubescout.py <server_address>`

For example:

`./client_cube_scout.py localhost`

Whenever a person is detected, the client runs the on_enter.sh script with the name of the person as the first parameter. You can do whatever you want in there, but as an example, the following script would just print the person's name:

```
echo $1
```
