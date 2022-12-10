import numpy as np
import open3d as o3d
'''
函数功能：检测test_points是否在points_set凸包内？
def is_in_convex_polyhedron(points_set: np.ndarray, test_points: np.ndarray):
'''
def conv_hull(points: np.ndarray,is_show=False):
    """
    生成凸包 参考文档：https://blog.csdn.net/io569417668/article/details/106274172
    :param points: 待生成凸包的点集
    :return: 索引 list
    """
    pcl = array_to_pointcloud(points)
    hull, lst = pcl.compute_convex_hull()
    if is_show:
        hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
        hull_ls.paint_uniform_color((1, 0, 0))
        o3d.visualization.draw_geometries([pcl, hull_ls])
    return lst

'''array_to_point_cloud是用来把NdArray类型的点坐标转换成o3d.geometry.PointCloud类型的函数'''
def array_to_pointcloud(np_array):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np_array)
    return pcd

def is_in_convex_polyhedron(points_set: np.ndarray, test_points: np.ndarray,is_show=False):
    """
    检测点是否在凸包内：
    原理：针对待判定的每个点，逐一加入原有点集，然后判断新形成的凸包的边界点集是否有改变？
    如果凸包点集没有变，说明新的点在凸包内；如果点集变了，说明待判断点在凸包外！
    :param points_set: 凸包，需要对分区的点进行凸包生成 具体见conv_hull函数
    :param test_points: 需要检测的点 可以是多个点
    :return: bool类型
    """
    assert type(points_set) == np.ndarray
    assert type(points_set) == np.ndarray
    bol = np.zeros((test_points.shape[0], 1), dtype=np.bool)
    ori_set = points_set
    ori_edge_index = conv_hull(ori_set)
    ori_edge_index = np.sort(np.unique(ori_edge_index))
    for i in range(test_points.shape[0]):
        new_set = np.concatenate((points_set, test_points[i, np.newaxis]), axis=0)
        new_edge_index = conv_hull(new_set,is_show)
        new_edge_index = np.sort(np.unique(new_edge_index)) #np.unique( )该函数是去除数组中的重复数字,并进行排序之后输出
        bol[i] = (new_edge_index.tolist() == ori_edge_index.tolist()) #
    return bol

if __name__ == '__main__':
    # test1
    A = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                  [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1],
                  [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1],
                  ])

    p = np.array([[5.5, .5, .5], [.2, .3, .6], [1, 1, 1.1]])
    print(is_in_convex_polyhedron(A, p,True))  # True True False

    # test2
    # path = r'D:\desktop\data\lower_jaw_data\points1.txt'
    # points_set = np.array(load_data_txt(path))
    # p = np.array([[2.31740, -0.72062, 12.51270], [115, 115, 115]])
    # print(in_convex_polyhedron(points_set, p))  # True, False
