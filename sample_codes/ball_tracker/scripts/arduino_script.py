#Arduino Node will subscribe ball_tracker node and send to arduino hardware

#!/usr/bin/env python
import rospy
from std_msgs.msg import String

#Serial module
import serial

ser=-1;

def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
    ser.write(str(data.data))

def listener():
    rospy.init_node('Arduino_Node', anonymous=True)
    rospy.Subscriber("ball_track", String, callback)
    rospy.spin()


def open_arduino(dev_name,baud_rate):
	try:
		global ser
		ser=serial.Serial(dev_name,baud_rate)		

		print "Arduino Port Opened"		

	except:
		print "Couldnt Open Arduino"


	

if __name__ == '__main__':

    open_arduino('/dev/ttyACM0',57600)

 

    try: 
    	listener()
    except rospy.ROSInterruptException:
        ser.close()
	pass

