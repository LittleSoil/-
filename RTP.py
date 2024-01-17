#导入geoist库
import matplotlib.pyplot as plt
from geoist import gridder
from geoist.inversion import geometry
from geoist.pfm import prism, pftrans, giutils
from geoist.vis import giplt

import numpy as np


#磁场方向,倾角inc（inclination）偏角（declination）
inc, dec = -46.401, -1.681
# 加载数据文件
data = np.loadtxt('EMAG.dat')
# 提取每一列数据
lat = data[:, 0]*1100  # 第一列
lon = data[:, 1]*1100  # 第二列
anomaly = data[:, 2]  # 第三列

#这里直接使用经纬度作为单位，注意到1°等于110km
#这样经度和纬度的的范围就是【100.02  104.98】 [24.02 34.98]
#需要用到函数pftrans.reduce_to_pole(x, y, tf, shape, inc, dec, sinc=inc, sdec=dec)
#shap是网格的大小，可以计算出来（104.98-100.02）/0.03=
shape = (221,81)

pole = pftrans.reduce_to_pole(lat, lon, anomaly, shape, inc, dec, sinc=inc, sdec=dec)

#绘制图像
# giplt.contourf(y, x, tf, shape, 30, cmap=plt.cm.RdBu_r)
# plt.title("Orignal")
# giplt.contourf(lat, lon,  anomaly, shape, 30, cmap=plt.cm.RdBu_r)
# plt.colorbar(pad=0).set_label('nT')

# plt.title("RTP")
# giplt.contourf(lat, lon,  pole, shape, 30, cmap=plt.cm.RdBu_r)
# plt.colorbar(pad=0).set_label('nT')

fig, axes = plt.subplots(1, 2, figsize=(8, 8))
for ax in axes:
    ax.set_aspect('equal')
plt.sca(axes[0])
plt.title("Original total field anomaly")
giplt.contourf(lat, lon, anomaly, shape, 30, cmap=plt.cm.RdBu_r)
plt.colorbar(pad=0).set_label('nT')
giplt.m2km()

plt.sca(axes[1])
plt.title("RTP")
giplt.contourf(lat, lon,  pole, shape, 30, cmap=plt.cm.RdBu_r)
plt.colorbar(pad=0).set_label('nT')
giplt.m2km()
plt.tight_layout()
plt.show()

########################################
#########################################
#将pre写入文件
np.savetxt('output.txt', pole, fmt='%f', delimiter='\t')
#%f是浮点型，\t表示列之间分隔符