# Surface Postprocessing
Aiming to present pressure and displacement measurements on irregular surfaces.

## 1. Generating the files
/`run_generate_output.py`/

The data to be used for plotting are generated and stored in Hierarchical Data Format (HDF5), which are optimize to contain large amounts of data.

For the moment, the test [Ackley function](https://en.wikipedia.org/wiki/Test_functions_for_optimization) is used to replicate the pressure values.

## 2. Data postprocessing
The data are provided in a discrete, randomly distributed pattern. In order to achieve a regular grid for plotting, it was decided to **interpolate** the available values.

The interpolation has been carried out with the 'scatteredInterpolant()' function. It generates a continuous function across the entire study domain. Other methods, like 'griddata()' or 'TriScatteredInterp()' can be used as an alternative. 

## 3. Plotting the surface
#### 3D-Scatterplot
The first, simplest approach was to perform a scatterplot of the geometry with the available data in the .h5 files, so that the correctness and quality of the data could be checked. The 'scatter3()' function was used.

![Cone_scatterplot](Plots/Scatterplot_cone.png)
![Cone_scatterplot top_view)](Plots/Scatterplot_cone2.png)

From the top view, it became evident that the data are not evenly distributed over the space. This has led to the previously explained interpolation.

#### 3D-Surface plot
The interpolated data (See `2. Data postprocessing`) can now be used to generate a regular grid with the function 'meshgrid()'. 

First, the grid is created between the minimum and maximum limits of the available X and Y geometry values. Then, values of the interpolated function can be obtained for every point in the XY-meshgrid: `Z = F(X,Y)`.

Now, the 'surf()' function can be called with the available parameters.

#### Pressure data over the 3D-Surface plot
Once the 3D-Surface is created with the geometry data, the measured pressure data can be incorporated in the form of colours over the surface. Once the pressure field has been interpolated and a regular mesh has been created with it, it can be added as an additional parameter in the 'surf()' function.

## 4. Plotting values on the surface
