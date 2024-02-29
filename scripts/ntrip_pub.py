import rospy
from mavros_msgs.msg import RTCM

def rtcm_callback(data):
    global pub
    pub.publish(data)
    print(data)
    print("----------------------------------------------")

def ntrip_to_mavros():
    global pub
    rospy.init_node('ntrip_to_mavros', anonymous=True)

    rospy.Subscriber('/ntrip_client/rtcm', RTCM, rtcm_callback)

    pub = rospy.Publisher('/mavros/gps_rtk/send_rtcm', RTCM, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    try:
        ntrip_to_mavros()
    except rospy.ROSInterruptException:
        pass
