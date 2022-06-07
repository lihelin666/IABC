# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

class plot3d:
    def __init__(self):
        self.fig=fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')

    def plot3dsphere(self,x0,y0,z0,r,nu,nv,isfig):
        # Make data 半年内
        u = np.linspace(0, 2 * np.pi, nu)
        v = np.linspace(0, np.pi, nv)
        x = r * np.outer(np.cos(u), np.sin(v))+x0
        y = r * np.outer(np.sin(u), np.sin(v))+y0
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))+z0

        # Plot the surface
        self.ax.plot_surface(x, y, z, color='b',cmap=plt.cm.jet,
                             rstride=1, cstride=1, linewidth=0)

        # self.ax.plot_wireframe(x,y,z)

    def plot3dscatter(self,x,y,z,**kwargs):
        self.ax.scatter(x, y, z,**kwargs)

    def show(self):
        # plt.legend()
        plt.show()

    def __del__(self):
        print('清空完成')

if __name__ == '__main__':
    p3=plot3d()
    p3.plot3dsphere(0,0,0,50,10,10,True)
    x = np.linspace(0, 100,10)
    y = np.linspace(0, 100,10)
    z = np.linspace(0, 100,10)
    p3.plot3dscatter(x,y,z)
    p3.show()
