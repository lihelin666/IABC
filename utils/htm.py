import numpy as np
from numpy import sin,cos,pi

'''
* 计算齐次坐标变换
'''
def getHTMMatrix(dx,dy,dz,a,b,c):
    from sympy import sin, cos
    '''
    计算其次坐标变换矩阵的公式
    注意！！！！！！！！！！！！
    np.asarray的矩阵乘法必须是使用np.dot
    ap.matrix的矩阵乘法可以使用 *
    :return:
    '''
    t = np.asarray([[cos(b) * cos(c), -sin(c) * cos(b), sin(b), dx],
                  [sin(a) * sin(b) * cos(c) + sin(c) * cos(a), -sin(a) * sin(b) * sin(c) + cos(a) * cos(c),-sin(a) * cos(b), dy],
                  [sin(a) * sin(c) - sin(b) * cos(a) * cos(c), sin(a) * cos(c) + sin(b) * sin(c) * cos(a),cos(a) * cos(b), dz],
                  [0, 0, 0, 1]])
    # print('HTM:',t)
    return t


def getHTMMatrixVal(dx,dy,dz,a,b,c):
    '''
    计算其次坐标变换矩阵的值
    注意！！！！！！！！！！！！
    np.asarray的矩阵乘法必须是使用np.dot
    ap.matrix的矩阵乘法可以使用 *
    :return:
    '''
    t = np.asarray([[cos(b) * cos(c), -sin(c) * cos(b), sin(b), dx],
                  [sin(a) * sin(b) * cos(c) + sin(c) * cos(a), -sin(a) * sin(b) * sin(c) + cos(a) * cos(c),-sin(a) * cos(b), dy],
                  [sin(a) * sin(c) - sin(b) * cos(a) * cos(c), sin(a) * cos(c) + sin(b) * sin(c) * cos(a),cos(a) * cos(b), dz],
                  [0, 0, 0, 1]])
    # print('HTM:',t)
    return t.astype('float64')

def getHMatrixFromXYZMatrix(m1):
    '''
    从xyz二维矩阵获取其次坐标矩阵，每一列是[X Y Z 1]
    :param m_33: np.matrix
    :return:
    '''
    m1_h = np.ones((m1.shape[0], m1.shape[1] + 1))
    m1_h[0:m1.shape[0], 0:m1.shape[1]] = m1
    return m1_h.T

def getHArrayFromXYZArray(arr_xyz):
    '''
    根据xyz的np.arr获取其其次坐标数组
    :param arr_xyz:
    :return:
    '''
    arr_xyz_h=np.ones((arr_xyz.shape[0],arr_xyz.shape[1]+1))
    arr_xyz_h[:,0:arr_xyz.shape[1]]=arr_xyz
    return arr_xyz_h

# 获取其次坐标变换矩阵的逆矩阵
def getInvHTM(T):
    '''
    :param T: np.array
    :return:
    '''
    t_r=T[0:3,0:3]
    t_p=T[0:3,3]
    t_r_t=t_r.T
    t_inv=np.zeros((4,4))
    # print(t_inv)
    t_inv[0:3,0:3]=t_r_t
    # print(t_inv)
    t_inv[0:3,3]=-np.dot(t_r_t,t_p)
    # print(t_inv)
    t_inv[3,3]=1
    return t_inv.astype('float64')

if __name__ == '__main__':
    # print(getHTMMatrixVal(0,1,2,1,1,1))
    # exit()
    from sympy import Symbol,print_latex
    dx = Symbol('dx')
    dy = Symbol('dy')
    dz = Symbol('dz')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    dx=0
    dy=0
    dz=0
    a=0
    c=0
    res=getHTMMatrix(dx,dy,dz,a,b,c)
    print_latex(res)
    # print(sympy.latex(res))
    exit()
    t=np.array([[-2.48275044e-01,  9.68616674e-01, -1.18747715e-02,
         7.30440000e+01],
       [-9.68685501e-01, -2.48290889e-01,  1.41582330e-04,
        -7.25910000e+01],
       [-2.81125927e-03,  1.15380704e-02,  9.99929359e-01,
        -4.49300000e+01],
       [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
         1.00000000e+00]])

    # t_inv=getInvHTM(t)
    # print(t_inv)
    # print(np.dot(t,t_inv))
    # print(np.dot(t_inv,t))


 #    t=np.asarray([[   73.044   ,-72.591,   -44.93 ],
 # [   48.163 , -169.674 ,  -44.68 ],
 # [   23.252,  -266.696,   -44.6  ],
 # [  381.892 , -877.003  ,  80.889],
 # [  356.956 , -974.228 ,   80.563],
 # [  332.026 ,-1071.512 ,   80.104]])
 #    print(t)
 #    arr=getHArrayFromXYZArray(t)
 #    print(arr)

    t=np.array([[1,1],[1,1]])
    l2=np.linalg.norm(t,2)
    print(l2)


