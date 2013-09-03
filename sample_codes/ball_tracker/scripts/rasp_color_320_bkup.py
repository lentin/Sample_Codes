#!/usr/bin/python

"""
This program demonstrate tracking of red ball and sending commands to arduino"


"""

#Importing headers

import rospy

from std_msgs.msg import String
import sys
import cv2.cv as cv



if __name__ == '__main__':




	global x_count

	global y_count		


	x_count=0
	y_count=0

#ROS Initialisation

	pub=rospy.Publisher('ball_track',String)


	rospy.init_node('Ball_Tracker')

	capture= cv.CreateCameraCapture(0)
	

	cv.NamedWindow("result",1)
	cv.NamedWindow("thr",1)
	width = 320

	height = 240

	#Setting width
	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)

	#Setting height

	cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height)

	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)


	while True:

		frame=cv.QueryFrame(capture)
		
		if not frame:

			cv.WaitKey(0)
			break;


		cv.Smooth(frame,frame,cv.CV_BLUR,3)
		
		hsv = cv.CreateImage(cv.GetSize(frame),8,3)
		
		cv.CvtColor(frame,hsv,cv.CV_BGR2HSV)

		thr = cv.CreateImage(cv.GetSize(frame),8 ,1)


		#Change threshold value				


		cv.InRangeS(hsv,(30,110,195),(40,160,255),thr) 

		moments = cv.Moments(cv.GetMat(thr,1),0)

		area = cv.GetCentralMoment(moments,0,0)

		cv.Line(frame,(160,0),(160,240),(0,0,255),3,8,0)

		if(area > 10000):


			x = cv.GetSpatialMoment(moments,1,0)/area
			y= cv.GetSpatialMoment(moments,0,1)/area


#			overlay = cv.CreateImage(cv.GetSize(frame),8,3)

			cv.Circle(frame,(int(x),int(y)),2,(255,255,255),20)


#			cv.Add(frame,overlay,frame)
	
#			cv.Merge(thr,None,None,None,frame)
			if(int(x) < 160):
				value = 160 - int(x)
				cv.PutText(frame,"Left["+str(value)+"]", (int(x),int(y)),font, (255,255,0))
				
				x_count+=1

				if(x_count > 10):			
					print "Left Offset=" , value

					pub_string="l"+chr(int(value))
					pub.publish(pub_string)
					x_count=0
			elif(int(x) > 160):
				value =  int(x) - 160
				cv.PutText(frame,"Right["+str(value)+"]", (int(x),int(y)),font, (0,255,0))

                                    
				y_count+=1
				if(y_count > 10):

					print "Right Offset=" , value
                                	pub_string="r"+chr(int(value))
                                	pub.publish(pub_string)
                                	y_count=0





		cv.ShowImage("result",frame)

		cv.ShowImage("thr",thr);
		if cv.WaitKey(10) == 27:

			break			


