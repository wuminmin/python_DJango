import gmplot
import pandas

import myConfig

gmap = gmplot.GoogleMapPlotter(30.428, 117.145, 16)
gmap.apikey = myConfig.google_apikey
df1 = pandas.read_excel(myConfig.django_root_path + '/cell_analyse/' + 'LTE扇区导出_20190220_120220_02385.xlsx', sheet_name=0)
latitudes = df1['扇区纬度']
longitudes = df1['扇区经度']
# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
# gmap.scatter(latitudes, longitudes, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
gmap.heatmap(latitudes, longitudes)

gmap.draw("mymap.html")