from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

class MultiStatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('multi_state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        loop_rate = self.create_rate(30)

        # robot state
        # tilt = 0.
        tinc = degree
        # swivel = 0.
        angle = 0.
        # height = 0.
        # hinc = 0.005

        left_front_wheel_joint = 0.
        right_front_wheel_joint = 0.
        left_back_wheel_joint = 0.
        right_back_wheel_joint = 0.

        # message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'base_link'
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['left_front_wheel_joint', 'right_front_wheel_joint',
                                    'left_back_wheel_joint', 'right_back_wheel_joint']
                joint_state.position = [left_front_wheel_joint, right_front_wheel_joint,
                                        left_back_wheel_joint, right_back_wheel_joint]

                # update transform
                # (moving in a circle with radius=2)
                odom_trans.header.stamp = now.to_msg()
                odom_trans.transform.translation.x = cos(angle)*0.5
                odom_trans.transform.translation.y = sin(angle)*0.5
                odom_trans.transform.translation.z = 0.
                odom_trans.transform.rotation = \
                    euler_to_quaternion(0, 0, angle + pi/2) # roll,pitch,yaw

                # send the joint state and transform
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)

                # Create new robot state
                # tilt += tinc
                # if tilt < -0.5 or tilt > 0.0:
                #     tinc *= -1
                # height += hinc
                # if height > 0.2 or height < 0.0:
                #     hinc *= -1
                # swivel += degree
                left_front_wheel_joint += tinc
                angle += degree/4


                # This will adjust as needed per iteration
                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main():
    node = MultiStatePublisher()

if __name__ == '__main__':
    main()
