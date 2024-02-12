#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

import time
from math import pi

class TurtleBot:

    def __init__(self):
        rospy.init_node('turtlebot_circle_driver', anonymous=True)

        # Reset TurtleBot3 in Gazebo
        rospy.wait_for_service('/gazebo/reset_world')
        reset_turtlebot = rospy.ServiceProxy('/gazebo/reset_world', Empty)
        reset_turtlebot()

        # Publisher for velocity commands
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.rate = rospy.Rate(10)

    def move_in_circle(self, radius, linear_speed):
        twist = Twist()
        twist.linear.x = linear_speed  # linear velocity
        angular_speed = linear_speed / radius  # Angular velocity for circular motion

        # Time to complete one circle
        rot_period = 2 * pi * radius / linear_speed

        # Start time
        start_time = rospy.get_time()

        while rospy.get_time() - start_time <= rot_period:
            twist.angular.z = angular_speed
            self.velocity_publisher.publish(twist)
            self.rate.sleep()

        # Stop motion after completing one circle
        twist.linear.x = 0
        twist.angular.z = 0
        self.velocity_publisher.publish(twist)

if __name__ == '__main__':
    try:
        turtlebot = TurtleBot()

        # Define parameters for the circle
        radius = 1.0  # Radius of the circle
        linear_speed = 0.5  # Linear speed

        rospy.loginfo("Moving TurtleBot3 Burger in a single circle...")
        turtlebot.move_in_circle(radius, linear_speed)

    except rospy.ROSInterruptException:
        pass

