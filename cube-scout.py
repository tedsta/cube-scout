#!/usr/bin/env python

import sys
import math
from cv2 import *
import numpy as np

def read_csv(filename):
    images = []
    labels = []
    names = {} # Maps person ID to name
    with open(filename, "r") as csv_file:
        for line in csv_file:
            columns = line.strip().split(";")
            if len(columns) != 2:
                continue # TODO: error message or something
            path = columns[0]
            label = int(columns[1])
            if label not in names: # New person! :D
                name = path.split("/")[-2]
                names[label] = name
            if path:
                images.append(cvtColor(imread(path, CV_LOAD_IMAGE_COLOR), COLOR_BGR2GRAY))
                labels.append(label)
    return images, labels, names

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def main():
    # Validate program arguments, print usage if invalid
    if len(sys.argv) < 4:
        print("usage: " + sys.argv[0] + " </path/to/haar_face> </path/to/haar_eye> </path/to/csv.ext> </path/to/device id>")
        print("\t </path/to/haar_face> -- Path to the Haar Cascade for face detection.")
        print("\t </path/to/csv.ext> -- Path to the CSV file with the face database.")
        print("\t <device id> -- The webcam device id to grab frames from.")
        exit()
    take_samples = False
    if "-s" in sys.argv:
        take_samples = True
    
    # Get the program arguments
    fn_haar_face = sys.argv[1]
    fn_csv = sys.argv[2]
    device_id = int(sys.argv[3])

    # Load the csv file
    print("Loading training data...")
    images = None
    labels = None
    try:
        images, labels, names = read_csv(fn_csv)
    except Exception as error:
        sys.stderr.write("Failed to open csv '"+fn_csv+"'. Reason: "+str(error)+"\n")

    # Get image dimensions
    im_width, im_height = images[0].shape

    # Create a FaceRecognizer and train it on the given images
    print("Training face recognizer...")
    model = createLBPHFaceRecognizer()
    model.train(images, np.asarray(labels))

    # Create classifier for face detection
    haar_face = CascadeClassifier()
    haar_face.load(fn_haar_face)

    print("Initializing video capture...")

    # Get a handle to the video device
    cap = VideoCapture(device_id)

    # Make sure we can use the video device
    if not cap.isOpened():
        sys.stderr.write("Failed to open video capture device: "+device_id+"\n")
        exit()

    image_sample_counter = 0
    
    while True:
        # Exit on escape key
        key = waitKey(10)
        if key == 27:
            break

        # frame holds the current frame of the video device
        _, frame = cap.read()

        # Clone the current frame
        original = frame.copy()

        # Convert the current frame into grayscale
        gray = cvtColor(original, COLOR_BGR2GRAY)

        # Find the faces in the frame
        faces = detect(gray, haar_face)

        # At this point we have the position of the faces in faces.
        # Now, we need to get the faces, make a prediction, and
        # annotate it in the video.
        for face in faces:
            # Unpack rect
            face_x1, face_y1, face_x2, face_y2 = face[0], face[1], face[2], face[3]

            # Crop the face from the image
            face_im = gray[face_y1:face_y2, face_x1:face_x2]

            # Resize face for Eigenfaces and Fisherfaces or whatever
            face_resized = resize(face_im, (im_width, im_height), 1.0, 1.0, INTER_CUBIC)

            # Now perform prediction
            prediction = model.predict(face_resized)

            # Write face image if we want
            if take_samples:
                face_im_color = original[face_y1:face_y2, face_x1:face_x2] 
                face_im_color = resize(face_im_color, (130, 130), 1.0, 1.0, INTER_CUBIC)
                print("Writing image...")
                imwrite("data/samples/sample"+str(image_sample_counter)+".jpg", face_im_color)
                image_sample_counter += 1

            ####################
            # Write info to original image
            rectangle(original, (face_x1, face_y1), (face_x2, face_y2), (0, 255, 0), 3)

            # Create the text to annotate the box
            box_text = ""
            if prediction:
                box_text = names[prediction[0]]+":"+str(100-math.floor(prediction[1]/255*100))+"%"

            # Calculate the position for the annotation text
            #text_x = max(face_x1 - 10, 0)
            #text_y = max(face_y1 - 10, 0)
            text_x = face_x1 - 10
            text_y = face_y1 - 10

            # Put the text into the image
            putText(original, box_text, (text_x, text_y), FONT_HERSHEY_PLAIN, 2.0, (0, 120, 255), 2)
        
        # Show the result
        imshow("face_recognizer", original)

if __name__ == "__main__":
    main()
