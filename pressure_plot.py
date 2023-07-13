import os
import h5py
import numpy as np
from scipy.interpolate import LinearNDInterpolator, griddata
from matplotlib import cm, mlab, ticker
import matplotlib.pyplot as plt

# file = os.path.join('TestOutput_CurvedShapes/output_files/ArchSupported0DegStruct_WTestValues.h5')
# file = os.path.join('TestOutput_CurvedShapes/output_files/Cone0DegStruct_WTestValues.h5')
file = os.path.join('TestOutput_CurvedShapes/output_files/Hypar0DegStruct_WTestValues.h5')
# file = os.path.join('TestOutput_CurvedShapes/output_files/RidgeValley0DegStruct_WTestValues.h5')

with h5py.File(file,'r') as h5f:
    geometry = np.asarray(h5f['ModelData']['Nodes']['Local']['Coordinates'])
    data = np.asarray(h5f['ResultsData']['NodalDataValues']['AUX_INDEX'])

print(geometry.shape)
print(data.shape)

x = geometry[:,0]
y = geometry[:,1]
z = geometry[:,2]

x_min = min(geometry[:,0])
x_max = max(geometry[:,0])
y_min = min(geometry[:,1])
y_max = max(geometry[:,1])

# MESHGRID
n = 50    # Number of grid points per dimension
x_grid = np.arange(x_min, x_max, (x_max-x_min)/n)
y_grid = np.arange(y_min, y_max, (y_max-y_min)/n)
z_grid = griddata((x,y), z, (x_grid,y_grid), method='linear')
X,Y = np.meshgrid(x_grid, y_grid)

# SORTING (now not necessary)
'''
sorting_key = np.lexsort((x, y))
geometry_sorted = geometry[sorting_key, :]
x_sort = geometry_sorted[:,0]
y_sort = geometry_sorted[:,1]
z_sort = geometry_sorted[:,2]
'''

########
# INTERPOLATION
F = LinearNDInterpolator((x, y), z)
P = LinearNDInterpolator((x,y), data)
Z = F(X,Y)
# Z = mlab
pressure = P(X,Y)
pressure[np.isnan(pressure)] = 0
 

########
# PLOTS

# Plot 1: 3D surface plot (colour: Z)
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(111, projection='3d')
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})   # 'figsize' and 'layout' arguments can be used here
plt.title('Surface plot')

surf1 = ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=1)

cbar1 = fig1.colorbar(surf1, shrink=0.5, aspect=5)
cbar1.set_label('z')


# Plot 2: 3D surface plot (colour: pressure)
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
plt.title('Surface plot w/ pressure data')

# my_col = cm.jet(pressure*0.1)
my_col = cm.coolwarm(pressure*0.1)

# surf2 = ax2.plot_surface(X, Y, Z,
#                          facecolors=cm.viridis(pressure*0.1), cmap=cm.coolwarm, linewidth=1,
#                          alpha=1)   # transparency
surf2 = ax2.plot_surface(X,Y,Z,
                         facecolors=my_col, cmap=cm.coolwarm, linewidth=0.5,    # cmap=cm.jet would also look good
                         alpha=1)

cbar2 = fig2.colorbar(surf2, shrink=0.5, aspect=5)
cbar2.set_label('Pressure')


# Plot 3: 3D surface plot + Pressure isolines
# this still does not work as expected !
fig3, ax3 = plt.subplots(subplot_kw={"projection": "3d"})
plt.title('Surface plot w/ isolines')

surf3 = ax3.plot_surface(X, Y, Z,
                       facecolors=my_col, cmap=cm.coolwarm, linewidth=1,       # cmap=cm.jet would also look good
                       alpha=1)   # transparency

levels = np.linspace(np.min(pressure), np.max(pressure), 30)  # number of isolines and their range
contour_lines = ax3.contour(X, Y, pressure, levels=levels, cmap=cm.Blues)    # offset=np.min(Z), zdir='z'

cbar3 = fig3.colorbar(surf3, shrink=0.5, aspect=5)
cbar3.set_label('Pressure')


# Plot 4: 2D geometric contour lines (a) - lines
fig4, ax4 = plt.subplots()
plt.title('Geometry contour lines')

levels = np.linspace(np.min(Z), np.max(Z), 50)  # number of isolines and their range

geom_contour1 = plt.contour(X, Y, Z, 40, cmap='jet')
# geom_contour = plt.tricontour(x,y,z, levels=levels)   # plt.contour delivers a cleaner result than triangulation
plt.clabel(geom_contour1, inline=True, fontsize=5)
cbar4 = plt.colorbar()
ticks = ticker.MaxNLocator(nbins=10)
cbar4.locator = ticks
cbar4.update_ticks()
cbar4.set_label('z')


# Plot 5: 2D geometric contour lines (b) - filled
fig5, ax5 = plt.subplots()
plt.title('Geometry contour lines')

plt.contourf(X, Y, Z, 50, cmap='RdGy_r')
cbar5 = plt.colorbar()
ticks = ticker.MaxNLocator(nbins=10)
cbar5.locator = ticks
cbar5.update_ticks()
cbar5.set_label('z')


# Plot 6: 2D geometric contour lines (c) - combined
fig6, ax6 = plt.subplots()
plt.title('Geometry contour')

geom_contour3 = plt.contour(X,Y,Z, 20, colors='black', linewidths=1.25)
plt.clabel(geom_contour3, inline=True, fontsize=5)

plt.imshow(Z, extent=[x_min,x_max,y_min,y_max], origin='lower', cmap='RdGy_r', alpha=0.6)
cbar6 = plt.colorbar()
cbar6.set_label('z')


# Plot 7: 2D pressure contour lines (a) - lines
fig7, ax7 = plt.subplots()
plt.title('Pressure contour lines')

pressure_contour1 = plt.contour(X,Y,pressure, 20, cmap='jet', linewidths=1.25)
plt.clabel(pressure_contour1, inline=True, fontsize=5)
cbar7 = plt.colorbar()
cbar7.set_label('Pressure')


# Plot 8: 2D pressure contour lines (b) - filled
fig8, ax8 = plt.subplots()
plt.title('Pressure contour lines')

plt.contourf(X,Y,pressure, 40, cmap='RdGy_r')
cbar8 = plt.colorbar()
cbar8.set_label('Pressure')


# Plot 9: 2D pressure contour plot (c) - combined
fig9, ax9 = plt.subplots()
plt.title('Pressure contour')

pressure_contour3 = plt.contour(X,Y,pressure, 16, colors='black', linewidths=1.0)
plt.clabel(pressure_contour3, inline=True, fontsize=5)

plt.imshow(pressure, extent=[x_min,x_max,y_min,y_max], origin='lower', cmap='RdGy_r', alpha=0.6)
cbar9 = plt.colorbar()
cbar9.set_label('Pressure')


# Plot 10: Comined 2D geometry & pressure plot
fig10, ax10 = plt.subplots()
plt.title('')

geom_contour3 = plt.contour(X,Y,Z, 20, colors='black', linewidths=1.25)
plt.clabel(geom_contour3, inline=True, fontsize=5)

plt.imshow(pressure, extent=[x_min,x_max,y_min,y_max], origin='lower', cmap='RdGy_r', alpha=0.6)
cbar10 = plt.colorbar()
cbar10.set_label('Pressure')


# Plot 11: Combined 2D geometry & pressure plot (inverted)
fig11, ax11 = plt.subplots()
plt.title('')

pressure_contour3 = plt.contour(X,Y,pressure, 20, colors='black', linewidths=1.0)
plt.clabel(pressure_contour3, inline=True, fontsize=5)

plt.imshow(Z, extent=[x_min,x_max,y_min,y_max], origin='lower', cmap='RdGy_r', alpha=0.6)
cbar11 = plt.colorbar()
cbar11.set_label('z')

plt.show()