"""

Entry Point to The App
Code for the backend Functions written in backend.py

What is the point of this App?
This app is a web app that can be used to detect emotions using python.

"""

import logging
import sys 
from tkinter import Tk, messagebox
import eel
import base64
from backend import * #import the backend

#Import Functions
from ML_methods.NueralNetwork import *
from ML_methods.LinearRegressionOneVariable import *
from ML_methods.LinearWithMultiVar import *
from ML_methods.SupervisedLearning import *
from ML_methods.UnsupervisedLearning import *
from ML_methods.Kmeans import *


def show_error(title, msg):
    root = Tk() # create a tkinter window
    root.withdraw()  # hide main window
    messagebox.showerror(title, msg) # show error message
    root.destroy() # destroy the tkinter window

def gen(camera):
    while True:
        frame = camera.get_frame() # get frame from camera
        """ Yield is a keyword in Python that is used to return 
        from a function without destroying the states of 
        its local variable """
        yield frame # yield the frame

@eel.expose
def video_feed():
    if VideoCamera.isOpened: 
        x = VideoCamera() # create a VideoCamera object
        y = gen(x) # create a generator object
        for each in y: # iterate through the generator object
            blob = base64.b64encode(each) # encode the frame
            blob = blob.decode("utf-8") # decode the frame
            eel.updateImageSrc(blob)() # update the image source
    else:
        print("Camera is not opened")

@eel.expose
def train(iterations):
    if Train_Model(int(iterations)): # train the model
        return "Model Was trained Successfully"
    
@eel.expose
def Close():
    VideoCamera().close_camera() #close the camera
    print("Camera Closed")
    
@eel.expose
def neuralNet():
    neuralNetwork()

@eel.expose
def linearRegressionOne():
    OneVarLinear()
    
@eel.expose
def linearRegressionMulti():
    MultiVarLinear()
    
@eel.expose
def supervisedLearning():
    SuperVised()

@eel.expose
def UnsupervisedLearning():
    DBSCAN_clustering()

@eel.expose 
def kmeansMethod():
    kmeans_visualizer()


def start_app():
    # Start the server 
    try:
        eel.init('Web') # path to project folder 
        eel.start('train.html') # start the web app with the main file index.html
    except Exception as e: 
        err_msg = 'Could not launch a local server' # error message
        logging.error('{}\n{}'.format(err_msg, e.args))
        show_error(title='Failed to initialise server',
                   msg=err_msg) #use tkinter to show error message
        sys.exit()


if __name__ == "__main__":
    start_app() # Call the start app function
    print("App Started")