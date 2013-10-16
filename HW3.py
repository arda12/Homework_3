
# Samira Ardani

# This code uses a netCDF file link server (e.g., http://apdrc.soest.hawaii.edu/dods/public_data/FRA-JCOPE2/el)
# and makes a plan-view using Basemap of some property found in the netCDF file.
# Then Makes timeseries using pandas of surface elevation as a time-variable property in the netCDF file, and plots this timeseries.

########################################################################################################

from datetime import datetime
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data=nc.Dataset("http://apdrc.soest.hawaii.edu/dods/public_data/FRA-JCOPE2/el")
data.variables.keys()
data.variables['el'].shape
el = data.variables['el'][0,0,:,:]
data.variables['el'].dimensions


lon = data.variables['lon'][:]
lat = data.variables['lat'][:]
lon,lat = np.meshgrid(lon,lat)

m = Basemap(llcrnrlon=107,llcrnrlat=10,urcrnrlon=179,urcrnrlat=62,projection='mill', lat_1=40)
x,y = m(lon,lat)

m.drawcoastlines()        
m.fillcontinents() 
m.drawcoastlines(linewidth = 0.2)
m.drawstates()
m.drawmeridians(np.arange(107,179,5),labels=[0,1,1,0])
m.drawparallels(np.arange(10,62,5),labels=[0,1,1,0])

# Plotting the plan view:
fig = plt.figure()
plt.contourf(x,y,el,cmap = plt.cm.RdBu_r)
plt.contourf(x,y,el,np.arange(-1,1.2,0.02),  cmap = plt.cm.RdBu_r)
m.fillcontinents()
cb = plt.colorbar(orientation='horizontal')
plt.title('Surface elevation in meter at 1/1/1993 ', fontsize =16 , style ='italic')

plt.show()
plt.savefig('plan_view.png')

# Making a Timeseries using Pandas:

dates = data.variables['time']
elev = data.variables['el'][:,0,8,8]
rng = pd.date_range('1/1/1993',periods=elev.size, freq='D')
ts1 = pd.Series(elev,index = rng)
data_frame = pd.DataFrame(ts1)

# Plotting the timeseries for point index: 8,8
data_frame.plot(figsize=(13.0, 9.0),legend = False)
plt.title('Daily Time series of surface elevation, 01-JAN-1993 to 31-DEC-2009 for a particular location', fontsize =16 , style ='italic')
plt.xlabel('Time (year)',fontsize =15)
plt.ylabel('Free surface elevation (m)',fontsize =15)
plt.subplots_adjust(bottom=0.15,left=0.1)
plt.show()
plt.savefig('surface_elev.png')