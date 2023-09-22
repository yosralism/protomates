#!/usr/bin/env python

#ROS STUFF
import rospy
from sensor_msgs.msg import Imu
from mavros_msgs.msg import VFR_HUD, GPSRAW
import message_filters

#MATH
import math
M_PI = 3.14159265358979323846

#LOGGING

from time import sleep
from time import time  
from os import path
from influxdb import InfluxDBClient

gps_type = ['GPS_FIX_TYPE_NO_GPS',
            'GPS_FIX_TYPE_NO_FIX',
            'GPS_FIX_TYPE_2D_FIX',
            'GPS_FIX_TYPE_3D_FIX',
            'GPS_FIX_TYPE_DGPS',
            'GPS_FIX_TYPE_RTK_FLOATR',
            'GPS_FIX_TYPE_RTK_FIXEDR',
            'GPS_FIX_TYPE_STATIC',
            'GPS_FIX_TYPE_PPP']

#influx configuration
ifuser = "protomates2"
ifpass = "123123"
ifdb   = "home"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "protomates2"

#sleep(300)
            
def pitch(q1,q2,q3,q4):
    
    t2 = +2.0 * (q4 * q2 - q3 * q1)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2

    return (math.asin(t2)*(180/M_PI)*-1)*100/90



def callback(gps_status, heading, imu):
    
    global filename, gps_type, ifuser, ifpass, ifdb, ifhost, ifport, measurement_name
    
    #timestamp = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(imu.header.stamp.secs))

    q1 = imu.orientation.x
    q2 = imu.orientation.y
    q3 = imu.orientation.z
    q4 = imu.orientation.w

    pitch_y = pitch(q1,q2,q3,q4)

 
    body = [
        {
            "measurement": measurement_name,
            "time": round(time() * 1000),
            "fields":{
                "latitude": gps_status.lat/10000000,
                "longitude": gps_status.lon/10000000,
                "slope": pitch_y,
                "heading": heading.heading,
                "fix_type": gps_type[gps_status.fix_type],
                "satellites_count" : gps_status.satellites_visible,
            }
        } 
    ]
    
    print(gps_status.lat/10000000)
    print(gps_status.lon/10000000)
    print(pitch_y)
    print(heading.heading)
    print(gps_type[gps_status.fix_type])
    print(gps_status.satellites_visible)

    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
    ifclient.write_points(body)

rospy.init_node('subscribe', anonymous=True)

gps_status_sub2 = message_filters.Subscriber('/mavros/gpsstatus/gps2/raw', GPSRAW)
heading_sub = message_filters.Subscriber('/mavros/vfr_hud', VFR_HUD)
imu_sub = message_filters.Subscriber('/mavros/imu/data', Imu)

ts = message_filters.ApproximateTimeSynchronizer([gps_status_sub2, heading_sub, imu_sub], 10, 0.1, allow_headerless=True)
ts.registerCallback(callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()





