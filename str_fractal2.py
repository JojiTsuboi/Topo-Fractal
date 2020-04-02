from stl import mesh
# from mpl_toolkits import mplot3d
# import matplotlib.pyplot as plt
import numpy as np

def show(data):
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(data.vectors))
    scale = data.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    plt.show()

data = mesh.Mesh.from_file('3retu_8point.stl')

show(data)