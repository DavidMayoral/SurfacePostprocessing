from KratosMultiphysics import AUX_INDEX
from kratos_utilities import ReadModelPart, WriteH5
import os


#################
# define you own function
import math


def get_position_based_value(x, y, z):
    '''
    return the 
    '''
    return -20.0 * math.exp(-0.2 * math.sqrt(0.5 * (x**2 + y**2)))-math.exp(0.5 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) + math.e + 20


#################
# generating data for input file with h5 output

input_folder = 'input_files'
input_files = ['ArchSupported0DegStruct.mdpa',
               'Cone0DegStruct.mdpa',
               'Hypar0DegStruct.mdpa',
               'RidgeValley0DegStruct.mdpa']
output_folder = 'output_files'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for in_file in input_files:

    # read in the MDPA file
    input_model_part = ReadModelPart(
        os.path.join(input_folder, in_file), in_file[:-5])

    for node in input_model_part.Nodes:
        cur_val = get_position_based_value(node.X0, node.Y0, node.Z0)
        node.SetValue(AUX_INDEX, cur_val)

    # output the H5 file
    WriteH5(os.path.join(output_folder,
            in_file[:-5] + '_WTestValues.h5'), input_model_part)
    del input_model_part

# read in the H5 file in pure python to manipulate
