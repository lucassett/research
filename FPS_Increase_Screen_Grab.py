# import the necessary packages
from __future__ import print_function
import datetime
import os
import time

time.sleep(3)

def printAndLog(info):
	print(info)
	f = open(os.path.join(args.dir, '00' + args.base + 'info.txt'), 'x')
	f.write(info)
	f.close

class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1
	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()
	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()

# import the necessary packages
from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
	def read(self):
		# return the frame most recently read
		return self.frame
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

# import the necessary packages
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("dir", type = str, help = "Directory to put frames in")
ap.add_argument("base", type = str, help = "Base file name")
ap.add_argument("-n", "--num-frames", type=int, default=250,
	help="# of frames to loop over for FPS test")
args = ap.parse_args()
if not os.path.exists(args.dir):
	os.mkdir(args.dir)


frames = []
# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()
# loop over some frames...this time using the threaded stream
while fps._numFrames < args.num_frames:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	frames.append(frame)
	# update the FPS counter
	fps.update()
# stop the timer and display FPS information to screen
fps.stop()

count = 1
for frame in frames:
        fname = os.path.join(args.dir, args.base + str(count) + ".png")
        cv2.imwrite(fname,frame)
        count += 1

info = "[INFO] elasped time: {:.2f}\n[INFO] approx. FPS: {:.2f}".format(fps.elapsed(),fps.fps())
printAndLog(info)

# do a bit of cleanup
vs.stop()