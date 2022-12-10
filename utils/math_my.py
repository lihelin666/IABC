import math
import numpy as np

'''根据四个坐标返回角度'''
def calc_angle(x1,y1,x2,y2):
    angle=0
    dy= y2-y1
    dx= x2-x1
    if dx==0 and dy>0:
        angle = 0
    if dx==0 and dy<0:
        angle = 180
    if dy==0 and dx>0:
        angle = 90
    if dy==0 and dx<0:
        angle = 270
    if dx>0 and dy>0:
       angle = math.atan(dy/dx)*180/math.pi
    elif dx<0 and dy>0:
       angle1 = math.atan(dy/dx)*180/math.pi
       angle=180 + angle1
    elif dx<0 and dy<0:
       angle = 180 + math.atan(dy/dx)*180/math.pi
    elif dx>0 and dy<0:
       angle = 360 + math.atan(dy/dx)*180/math.pi
    return angle*math.pi/180

'''计算nparr的角度'''
def cal_angle_by_pd(x1a,y1a,x2a,y2a):
    res=[]
    for i in range(len(x1a)):
        # print(x1a.iloc[i],y1a.iloc[i],x2a.iloc[i],y2a.iloc[i])
        res.append(calc_angle(x1a.iloc[i],y1a.iloc[i],x2a.iloc[i],y2a.iloc[i]))
    return np.asarray(res)