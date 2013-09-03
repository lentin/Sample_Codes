#!/usr/bin/python

"""
This program demonstrate tracking of red ball and sending commands to arduino"


"""

#Importing headers

import rospy

from std_msgs.msg import String
import sys
import cv2.cv as cv
import time

x_co = 0
y_co = 0

h1=0
h2=0

s1=0
s2=0

v1=0
v2=0
count = 0

def on_mouse(event,x,y,flag,param):
  global x_co
  global y_co
  if(event==cv.CV_EVENT_LBUTTONDOWN):
    x_co=x
    y_co=y 
    
    print "Left button clicked "
	
  if(event==cv.CV_EVENT_RBUTTONDOWN):
    global count
    count=0
    print "Right button clicked"



if __name__ == '__main__':




	global x_count

	global y_count		


	x_count=0
	y_count=0

#ROS Initialisation

	pub=rospy.Publisher('ball_track',String)


	rospy.init_node('Ball_Tracker')

	capture= cv.CreateCameraCapture(0)
	

	cv.NamedWindow("result",1);


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


		cv.InRangeS(hsv,(h1,s1,v1),(h2,s2,v2),thr) 

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
			if(int(x) < 130):
				value = 130 - int(x)
				cv.PutText(frame,"Left["+str(value)+"]", (int(x),int(y)),font, (255,255,0))
				
				x_count+=1

				if(x_count > 2):			
					print "Left Offset=" , value
					pub_string="r"+chr(int(value))
					pub.publish(pub_string)
					x_count=0

			if(int(x) > 190):
				value =  int(x) -190
				cv.PutText(frame,"Right["+str(value)+"]", (int(x),int(y)),font, (0,255,0))

                                    
				y_count+=1
				if(y_count > 2):

 					pub_string="l"+chr(int(value))
                                	pub.publish(pub_string)
                                	y_count=0
					print "Right Offset=" , value

			elif(int(x) < 190 and int(x) > 130):
				value=30

				cv.PutText(frame,"Center["+str(value)+"]", (int(x),int(y)),font, (0,255,0))
 				pub_string="c"+chr(int(value))
                                pub.publish(pub_string)
                                print "Center",value

				


		cv.SetMouseCallback("result",on_mouse, 0);
		if(count == 0):		
    			s=cv.Get2D(hsv,y_co,x_co)
		
			h1=s[0]-40
			h2=s[0]+40


			s1=s[1]-40
			s2=s[1]+40

			v1=s[2]-40
			v2=s[2]+40
			


			count =1


#		print "H1:",h1,"      S1:",s1,"       V1:",v1
#    		print "H2:",h2,"      S2:",s2,"       V2:",v2


#    		cv.PutText(frame,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),font, (55,25,255))



		cv.ShowImage("result",frame)


		if cv.WaitKey(10) == 27:

			break			


