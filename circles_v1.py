import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
from websocket import create_connection

def returnResult(x,y,w,h,img,winName):

	x1,y1,w1,h1 = x,y,w,h
	cropImage1 = img[x1:x1+w1,y1:y1+h1]
	bwImage1 = cv2.cvtColor(cropImage1, cv2.COLOR_BGR2GRAY)
	ret1,th1 = cv2.threshold(bwImage1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	cv2.imshow(winName,th1)
	foreground1 = th1.sum()/255.0
	#print foreground
	totalPixels1 = w1*h1
	#if (winName == 'CropWindow1'):

	#	print foreground1, totalPixels1
	# Display the resulting frame
	if foreground1 < 0.45 * totalPixels1:
		cv2.imshow(winName,cropImage1)
		bit1 = 1
		#ws.send(str(bit))
		print foreground1, totalPixels1
		#print fNum
	else:
		bit1 = 0
		#ws.send(str(bit))
	return bit1

class Cam():

  def __init__(self, url):
    
    self.stream = requests.get(url, stream=True)
    self.thread_cancelled = False
    self.thread = Thread(target=self.run)
    print "camera initialised"

    
  def start(self):
    self.thread.start()
    print "camera stream started"

  
  def run(self):
	bytes=''
	fnum = 1
	bit = 0
	#cnt = 0;
	while not self.thread_cancelled:
		try:
			bytes+=self.stream.raw.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
			  jpg = bytes[a:b+2]
			  bytes= bytes[b+2:]
			  img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
			  #cv2.imshow('cam',img)
			  #cv2.imwrite('test2/'+str(cnt) + '.jpg',img)
			  #cnt = cnt + 1
			  if cv2.waitKey(1) ==27:
				exit(0)
			  ##begin Code
			  frame = img
			  x1,y1,w1,h1 = 263,1129,100,76
			  x2,y2,w2,h2 = 728,847,73,103
			  x3,y3,w3,h3 = 711,317,86,98
			  x4,y4,w4,h4 = 297,74,86,86
			  bit1 = returnResult(x1,y1,w1,h1,frame,'CropWindow1')
			  bit2 = returnResult(x2,y2,w2,h2,frame,'CropWindow2')
			  bit3 = returnResult(x3,y3,w3,h3,frame,'CropWindow3')
			  bit4 = returnResult(x4,y4,w4,h4,frame,'CropWindow4')
			  finalMsg = str(bit1) + ' ' +str(bit2) + ' ' + str(bit3) + ' ' +str(bit4)
			  ws.send(finalMsg)
			  ## End code
			  if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except ThreadError:
			self.thread_cancelled = True
	ws.close()
  def is_running(self):
    return self.thread.isAlive()
      
    
  def shut_down(self):
    self.thread_cancelled = True
    #block while waiting for thread to terminate
    while self.thread.isAlive():
      time.sleep(1)
    return True

  
    
if __name__ == "__main__":
  url = 'http://192.168.1.215/axis-cgi/mjpg/video.cgi'
  cam = Cam(url)
  ws = create_connection("ws://128.113.20.15:1380")
  cam.start()
