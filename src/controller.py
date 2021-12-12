from time import time
import rospy
from std_msgs.msg import Float64
import math
from control_msgs.msg import JointControllerState
from gazebo_msgs.srv import GetLinkState
import numpy as np

model_info= rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)  
def getGoals():
    global model_info, Goals
    Goals = []

    Goal_names= ["unit_cylinder::link", "unit_box::link", "unit_sphere::link"]
    for i in Goal_names:
        obj = model_info(i,"world")
        x = obj.link_state.pose.position.x
        y = obj.link_state.pose.position.y
        z = obj.link_state.pose.position.z + 0.1
        Goals.append([x, y, z])
    Goals = np.array(Goals)

def loc():

    model_info1 = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState) 
    obj1 = model_info1("my_robot::rm3_Link","world")
    xl = obj1.link_state.pose.position.x
    yl = obj1.link_state.pose.position.y
    zl = obj1.link_state.pose.position.z
    print(xl,yl,zl)


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
        curr_pos = model_info("my_robot::dummy_link","world")
        curr_x = curr_pos.link_state.pose.position.x
        curr_y = curr_pos.link_state.pose.position.y
        # curr_z = curr_pos.link_state.pose.position.z

        mov_x = Goals[0][0]-curr_x
        mov_y = Goals[0][1]-curr_y
        # mov_z = Goals[0][2]-curr_z 
        if(abs(mov_x)+abs(mov_y)<0.5):
            print(Goals[0][0],Goals[0][1])
            print(curr_x,curr_y)
            print("Reached goal")
            break
        elif(mov_x>0.5):
            print("for")
            mv_for(p)
        elif(mov_x<-0.5):
            print("bac")
            mv_back(p)
        elif(mov_y>0.5):
            print("right")
            mv_r(p)
        elif(mov_y<-0.5):
            print("left")
            mv_l(p)
        else:
            print(Goals[0][0],Goals[0][1])
            print(curr_x,curr_y)
            print("Reached end of if")
            break




def up(p):
    p[0][1].publish(-0.5)
    p[1][1].publish(-0.5)
    p[2][1].publish(-0.5)
    p[3][1].publish(0.5)
    p[4][1].publish(0.5)
    p[5][1].publish(0.5)

def mv_for(p):
    rate = rospy.Rate(3)
    p[1][1].publish(-0.5)
    p[3][1].publish(0.5)
    p[5][1].publish(0.5)

    rate.sleep()

    p[1][0].publish(0.5)
    p[3][0].publish(-0.5)
    p[5][0].publish(-0.5)

    rate.sleep()

    p[1][1].publish(0.01)
    p[3][1].publish(0.01)
    p[5][1].publish(0.01)

    rate.sleep()

    p[4][1].publish(0.5)
    p[0][1].publish(-0.5)
    p[2][1].publish(-0.5)

    rate.sleep()

    p[1][0].publish(0.01)
    p[3][0].publish(0.01)
    p[5][0].publish(0.01)

    rate.sleep()


    p[4][0].publish(-0.5)
    p[0][0].publish(0.5)
    p[2][0].publish(0.5)

    rate.sleep()

    p[4][1].publish(0.01)
    p[0][1].publish(0.01)
    p[2][1].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.01)
    p[0][0].publish(0.01)
    p[2][0].publish(0.01)

def mv_back(p):
    rate = rospy.Rate(3)
    p[1][1].publish(-0.5)
    p[3][1].publish(0.5)
    p[5][1].publish(0.5)

    rate.sleep()

    p[1][0].publish(-0.5)
    p[3][0].publish(0.5)
    p[5][0].publish(0.5)

    rate.sleep()

    p[1][1].publish(0.01)
    p[3][1].publish(0.01)
    p[5][1].publish(0.01)

    rate.sleep()

    p[4][1].publish(0.5)
    p[0][1].publish(-0.5)
    p[2][1].publish(-0.5)

    rate.sleep()

    p[1][0].publish(0.01)
    p[3][0].publish(0.01)
    p[5][0].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.5)
    p[0][0].publish(-0.5)
    p[2][0].publish(-0.5)

    rate.sleep()

    p[4][1].publish(0.01)
    p[0][1].publish(0.01)
    p[2][1].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.01)
    p[0][0].publish(0.01)
    p[2][0].publish(0.01)

def mv_r(p):
    rate = rospy.Rate(3)
    p[1][1].publish(-0.5)
    p[3][1].publish(0.5)
    p[5][1].publish(0.5)

    rate.sleep()

    p[1][0].publish(-0.5)
    p[3][0].publish(0.5)
    p[5][0].publish(0.5)

    rate.sleep()

    p[1][1].publish(0.01)
    p[3][1].publish(0.01)
    p[5][1].publish(0.01)

    rate.sleep()

    p[4][1].publish(0.5)
    p[0][1].publish(-0.5)
    p[2][1].publish(-0.5)

    rate.sleep()

    p[1][0].publish(0.01)
    p[3][0].publish(0.01)
    p[5][0].publish(0.01)

    rate.sleep()


    p[4][0].publish(0.5)
    p[0][0].publish(-0.5)
    p[2][0].publish(-0.5)

    rate.sleep()

    p[4][1].publish(0.01)
    p[0][1].publish(0.01)
    p[2][1].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.01)
    p[0][0].publish(0.01)
    p[2][0].publish(0.01)

def mv_l(p):
    rate = rospy.Rate(3)
    p[1][1].publish(-0.5)
    p[3][1].publish(0.5)
    p[5][1].publish(0.5)

    rate.sleep()

    p[1][0].publish(-0.5)
    p[3][0].publish(0.5)
    p[5][0].publish(0.5)

    rate.sleep()

    p[1][1].publish(0.01)
    p[3][1].publish(0.01)
    p[5][1].publish(0.01)

    rate.sleep()

    p[4][1].publish(0.5)
    p[0][1].publish(-0.5)
    p[2][1].publish(-0.5)

    rate.sleep()

    p[1][0].publish(0.01)
    p[3][0].publish(0.01)
    p[5][0].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.5)
    p[0][0].publish(-0.5)
    p[2][0].publish(-0.5)

    rate.sleep()

    p[4][1].publish(0.01)
    p[0][1].publish(0.01)
    p[2][1].publish(0.01)

    rate.sleep()

    p[4][0].publish(0.01)
    p[0][0].publish(0.01)
    p[2][0].publish(0.01)




# def mv_back(p):
def home(p):
    for i in range(6):
        for j in range(3):
            p[i][j].publish(0.01)
            

if __name__ == '__main__': 
    try:
        # getGoals()
        # traj()
        # pub()
        loc()
    except rospy.ROSInterruptException:
        pass