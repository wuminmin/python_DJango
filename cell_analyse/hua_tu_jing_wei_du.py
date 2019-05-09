# coding=utf-8
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

from myConfig import django_root_path


def DrawPointMap(file_name):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1,0.1,0.8,0.8])#[left,bottom,width,height]
    map = Basemap(projection='mill',lat_0=36,lon_0=122,\
                 llcrnrlat=30.5 ,urcrnrlat=35.3,llcrnrlon=116.2,urcrnrlon=121.99,\
			     ax=ax1,rsphere=6371200.,resolution='h',area_thresh=1000000)
    shp_info = map.readshapefile(django_root_path + '/cell_analyse' + '/' + 'gadm36_CHN_shp/gadm36_CHN_3', 'states', drawbounds=False)
    for info, shp in zip(map.states_info, map.states):
        proid = info['NAME_1']
        if proid == 'Jiangsu':
            poly = Polygon(shp,facecolor='w',edgecolor='k', lw=1.0, alpha=0.1)#注意设置透明度alpha，否则点会被地图覆盖
            ax1.add_patch(poly)
    parallels = np.arange(30.6,35.3,2)
    map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10) #parallels
    meridians = np.arange(116.3,122,2)
    map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10) #meridians
    posi = pd.read_csv(file_name)
    lat = np.array(posi["lat"][0:48])#获取经纬度坐标，一共有48个数据
    lon = np.array(posi["lon"][0:48])
    val = np.array(posi["val"][0:48],dtype=float)#获取数值
    size = (val-np.min(val)+0.05)*800#对点的数值作离散化，使得大小的显示明显
    x,y = map(lon,lat)
    map.scatter(x, y, s=size, color = 'r') #要标记的点的坐标、大小及颜色
    for i in range(0,47):
       plt.text(x[i]+5000,y[i]+5000,str(val[i]))
       #plt.text(lat[i],lon[i],str(val[i]), family='serif', style='italic', ha='right', wrap=True)
    #plt.annotate(s=3.33,xy=(x,y),xytext=None, xycoords='data',textcoords='offset points', arrowprops=None,fontsize=16)
    map.drawmapboundary()  #边界线
    #map.fillcontinents()
    map.drawstates()
    #map.drawcoastlines()  #海岸线
    map.drawcountries()
    map.drawcounties()
    plt.title('Jiangsu in CHINA')#标题
    plt.savefig('Jiangsu.png', dpi=100, bbox_inches='tight')#文件命名为Jiangsu.png存储
    plt.show()
if __name__=='__main__':
    DrawPointMap("Info.csv")
