import open3d as o3d
import numpy as np
import pandas as pd
import datatable

'''Dispalay an Open3d instance'''
def displayO3dIns(pcd,is_show_normal=False):
    o3d.visualization.draw_geometries([pcd],point_show_normal=is_show_normal)

def displayInlierOutlier(cloud, ind,is_show_normal=False):
    '''ref: http://www.open3d.org/docs/release/tutorial/geometry/pointcloud_outlier_removal.html'''
    print("Showing outliers (red) and inliers (gray): ")
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      point_show_normal=is_show_normal)

if __name__ == '__main__':
    fname=r"../data_real/2022-1-18pre/win2_calibrated.xyz"
    # load data with high speed
    ndarr = datatable.fread(fname, nthreads=-1).to_numpy()
    print(ndarr.shape)
    pts = ndarr[:, 0:3]
    normals = ndarr[:, 3:]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)

    pcd = pcd.voxel_down_sample(voxel_size=0.05)
    # Estimate normals
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=100))
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20,std_ratio=3.0)
    displayInlierOutlier(pcd, ind)