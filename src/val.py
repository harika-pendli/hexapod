from time import time
import rospy
from std_msgs.msg import Float64
import math
from control_msgs.msg import JointControllerState
from gazebo_msgs.srv import GetLinkState
import numpy as np
import math as m
global p
def traj():
    name = [["right_front_1", "right_front_2","right_front_3"],
    ["right_middle_1", "right_middle_2", "right_middle_3"],
    ["right_back_1",   "right_back_2",   "right_back_3"],
    ["left_front_1",   "left_front_2",  "left_front_3"],
    ["left_middle_1",  "left_middle_2", "left_middle_3"],
    ["left_back_1",    "left_back_2",   "left_back_3"]]
    p = []
    for i in range(6):
        p.append([])
        for j in range(3):
            p[i].append([])
            p[i][j] = rospy.Publisher('/hexapod/'+name[i][j]+'/command', Float64, queue_size=10)
    rospy.init_node('pub', anonymous=True)
    while not rospy.is_shutdown():
        cnt = 0
        if cnt==0:
            # home(p)
            cnt = cnt+1
            gait(p)
            # fdval(p)
            # t1,t2,t3 = ik(0,65,60)
            # print(t1,1.57-t2,1.57-t3)
        # ikval(t1,1.57-t2,1.57-t3,p)
            # 

def gait(p):
    rate = rospy.Rate(3)
    p[1][0].publish(0.01)
    p[3][0].publish(0.01)
    p[5][0].publish(0.01)

    rate.sleep()


    p[4][0].publish(-0.5)
    p[0][0].publish(0.5)
    p[2][0].publish(0.5)


def ik(x,y,z):
    a1 = 65
    a2 = 65
    r = m.sqrt(y*y+z*z)
    al = m.atan(z/y)
    bt = m.acos((a2*a2-a1*a1-r*r)/(-2*a1*r))
    t2 = bt-al
    t3 = m.radians(180) - m.acos((r*r-a1*a1-a2*a2)/(-2*a1*a2))
    t1 = m.atan(x/y)
    return m.degrees(t1),m.degrees(t2),m.degrees(t3)


def fdval(p):
    # p[1][1].publish(-0.5)
    # p[1][2].publish(0.5)
    # p[1][2].publish(0)
    p[1][1].publish(math.radians(-36.182))
    p[1][2].publish(math.radians(33.918))
    loc()

def ikval(t1,t2,t3,p):
    p[1][0].publish(t1)
    p[1][1].publish(t2)
    p[1][1].publish(t3)

def loc():
    model_info1 = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState) 
    obj1 = model_info1("my_robot::rm3_Link","world")
    xl = obj1.link_state.pose.position.x
    yl = obj1.link_state.pose.position.y
    zl = obj1.link_state.pose.position.z
    print(xl,yl,zl)

def home(p):
    for i in range(6):
        for j in range(3):
            p[i][j].publish(0)

if __name__ == '__main__': 
    try:
        # getGoals()
        traj()
        # pub()
    except rospy.ROSInterruptException:
        pass