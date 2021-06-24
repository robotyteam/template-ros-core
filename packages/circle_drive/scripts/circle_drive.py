#!/usr/bin/env python3
import os
import rospy
from std_msgs.msg import Bool
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import Twist2DStamped, StopLineReading

class MyNode(DTROS):

    def __init__(self, node_name):
        super(MyNode, self).__init__(node_name=node_name, node_type=NodeType.DEBUG)
        self.pub = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)
        self.sub_fw = rospy.Subscriber("go_forward", Bool, self.cb_fw)
        self.sub_bw = rospy.Subscriber("go_backward", Bool, self.cb_bw)



    def cb_fw(self, msg):
        rospy.loginfo("cd_fw")
        rate = rospy.Rate(0.5)
        msg = Twist2DStamped()
        msg.v = 0.5
        msg.omega = 0.0
        rospy.loginfo("Publishing message")
        self.pub.publish(msg)
        rate.sleep()
        msg.v = 0.0
        rospy.loginfo("Publishing message")
        self.pub.publish(msg)
    
    def cb_bw(self, msg):
        rospy.loginfo("cd_bw")
        rate = rospy.Rate(0.5)
        msg = Twist2DStamped()
        msg.v = -0.5
        msg.omega = 0.0
        rospy.loginfo("Publishing message")
        self.pub.publish(msg)
        rate.sleep()
        msg.v = 0.0
        rospy.loginfo("Publishing message")
        self.pub.publish(msg)



    def run(self):
        # publish message every 1 second
        rate = rospy.Rate(0.5) # 1Hz
        while not rospy.is_shutdown():
            self.cb_bw(None)
            rate.sleep()
            self.cb_fw(None)
            rate.sleep()

if __name__ == '__main__':
    # create the node
    node = MyNode(node_name='circle_drive_node')
    # run node
    node.run()
    # keep spinning
    rospy.spin()
