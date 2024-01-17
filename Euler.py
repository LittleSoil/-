#导入geoist库
from geoist.pfm import sphere, pftrans, euler, giutils
from geoist import gridder
from geoist.inversion import geometry
from geoist.vis import giplt
import matplotlib.pyplot as plt

import numpy as np
# 加载数据文件
originaldata = np.loadtxt('EMAG.dat')
# 提取每一列数据
lat = originaldata[:, 0]*1100  # 第一列
lon = originaldata[:, 1]*1100  # 第二列
z = np.full_like(lon, 4000) #第三列
anomaly = originaldata[:, 2]  # 第四列
inc, dec = -46.401, -1.681

data = np.column_stack((lat, lon, z, anomaly))

shape = (221,81)

xderiv = pftrans.derivx(lat, lon, anomaly, shape)
yderiv = pftrans.derivy(lat, lon, anomaly, shape)
zderiv = pftrans.derivz(lat, lon, anomaly, shape)

solver = euler.EulerDeconvMW(lat, lon, z, anomaly, xderiv, yderiv, zderiv,
                             structural_index=3, windows=(10, 20),
                             size=(1000, 500))

# Use the fit() method to obtain the estimates
solver.fit()

# The estimated positions are stored as a list of [x, y, z] coordinates
# (actually a 2D numpy array)
print('Kept Euler solutions after the moving window scheme:')
print(solver.estimate_)

# Plot the solutions on top of the magnetic data. Remember that the true depths
# of the center of these sources is 1500 m and 1000 m.

# plt.figure(figsize=(6, 5))
# plt.title('Euler deconvolution with a moving window')
# plt.contourf(lon.reshape(shape), lat.reshape(shape), anomaly.reshape(shape), 30,
#              cmap="RdBu_r")
# plt.scatter(solver.estimate_[:, 1], solver.estimate_[:, 0],
#             s=50, c=solver.estimate_[:, 2], cmap='cubehelix')
# plt.colorbar(pad=0).set_label('Depth (m)')

# plt.tight_layout()
# plt.show()

plt.figure(figsize=(6, 5))
plt.title('Euler deconvolution with a moving window')
plt.contourf(lat.reshape(shape) / 1100, lon.reshape(shape) / 1100, anomaly.reshape(shape), 30,
             cmap="RdBu_r")  # 将lat和lon除以1100
plt.scatter(solver.estimate_[:, 0] / 1100, solver.estimate_[:, 1] / 1100,  # 将坐标轴除以1100
            s=50, c=solver.estimate_[:, 2], cmap='cubehelix')
plt.colorbar(pad=0).set_label('Depth (m)')

plt.tight_layout()
plt.show()

