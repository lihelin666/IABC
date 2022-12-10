import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
# 二维绘图：https://www.runoob.com/numpy/numpy-matplotlib.html
# 三维绘图：https://blog.csdn.net/jasonzhoujx/article/details/81780774
# 3位绘图 https://www.jianshu.com/p/993cb9367737

from mpl_toolkits.mplot3d import Axes3D

def plot1d(y,title='',**kwargs):
    plt.figure()
    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Y axis")
    x=np.arange(0,len(y))
    plt.plot(x, y, "ob",linestyle="-") # 显示原点
    plt.show()

def plot2d(x,y,title='',**kwargs):
    plt.figure()
    plt.title(title)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.plot(x, y, "ob",linestyle="-") # 显示原点
    plt.show()

def scatter2d(x,y,title=""):
    plt.title(title)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.scatter(x, y) # 显示原点
    plt.show()

def plot3d(x,y,z,**kwargs):
    plt.title('Title')
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    # plt.zlabel("Z Axis")
    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z,'grey')
    plt.show()

def scatter3d(x,y,z,**kwargs):
    plt.title('Title')
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    # plt.zlabel("Z Axis")
    ax = plt.axes(projection='3d')
    ax.plot3D(x,y,z)
    ax.scatter3D(x, y, z, c=z, cmap='Greens')
    plt.show()

def scatter3dByNpArr(nparr_xyz,**kwargs):
    arr=np.asarray(nparr_xyz)
    [x,y,z]=[arr[:,0],arr[:,1],arr[:,2]]
    scatter3d(x,y,z)

def quiver3dCS(nparr,length=35):
    [x, y, z, dx, dy, dz] = [np.zeros(3), np.zeros(3), np.zeros(3), nparr[:, 0], nparr[:, 1], nparr[:, 2]]
    quiver3d(x, y, z, dx, dy, dz, length=length)


def quiver3dByArr(arr_3d_xyzdxdydz,length=35,**kwargs):
    arr=np.asarray(arr_3d_xyzdxdydz)
    [x,y,z,dx,dy,dz]=[arr[:,0],arr[:,1],arr[:,2],arr[:,3],arr[:,4],arr[:,5]]
    quiver3d(x,y,z,dx,dy,dz,length=length)

def quiver3d(x,y,z,dx,dy,dz,xlabel='',ylabel='',length=35,**kwargs):
    plt.title(f"{xlabel}-{ylabel}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax = plt.axes(projection='3d')
    ax.scatter3D(x, y, z, c='royalblue')
    ax.quiver(x, y, z, dx*length, dy*length, dz*length,color="lightcoral")  # normalize控制箭头的长短
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    plt.show()

if __name__ == '__main__':
    # x = np.arange(1, 11)
    # y = 2 * x + 5
    # plot2d(x,y)
    # plot1d(y)

    # 三维线的数据
    # zline = np.linspace(0, 15, 1000)
    # xline = np.sin(zline)
    # yline = np.cos(zline)
    # plot3d(xline,yline,zline)
    #
    # zdata = 15 * np.random.random(100)
    # xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
    # ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
    # scatter3D(xdata,ydata,zdata)
    arr=np.asarray([
        [1,2,3,1,2,3],
        [2,2,4,4,5,6],
        [5,2,4,4,5,6],
    ])
    quiver3dByArr(arr,length=1)
    print(arr[:,2])