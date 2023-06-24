'''
    Check the content of an H5 file for structure for example with HDFCompass
'''

import os
import numpy as np
import h5py


initial_filename = os.path.join('output_files', 'Hypar0DegStruct_WTestValues.h5')
with h5py.File(initial_filename, 'r') as h5f:
    nodal_data = np.asarray(h5f['ResultsData']['NodalDataValues']['AUX_INDEX'])
    geometry = np.asarray(h5f['ModelData']['Nodes']['Local']['Coordinates'])
    

# print(nodal_data[:10])
for i in range(0, geometry.shape[0], 100):
    print(geometry[i])

# print(nodal_data.shape)
# print(geometry.shape)