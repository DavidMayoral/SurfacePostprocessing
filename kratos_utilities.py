"""
It is the easiest to install the python packages for Kratos

Use this:

    Tried with python 3.9, 3.10, 3.11 from Microsoft Store on Windows 11, did not work.
    
    Works on Ubuntu 22 with the Kratos Developer version.
    
    

    # Python 3.9 with Kratos 9.2.2
    # only those which are actually necessary for you now
    python3.9 -m pip install --upgrade --force-reinstall --no-cache-dir KratosMultiphysics==9.2.2
    python3.9 -m pip install --upgrade --force-reinstall --no-cache-dir KratosStructuralMechanicsApplication==9.2.2
    python3.9 -m pip install --upgrade --force-reinstall --no-cache-dir KratosHDF5Application==9.2.2

    I get the error in KratosHDF5.HDF5FileSerial: Unsupported (Windows) "file_driver": sec2


    # Python 3.10 with Kratos 9.3.2
    # only those which are actually necessary for you now
    python3.10 -m pip install --upgrade --force-reinstall --no-cache-dir KratosMultiphysics==9.3.2
    python3.10 -m pip install --upgrade --force-reinstall --no-cache-dir KratosStructuralMechanicsApplication==9.3.2
    python3.10 -m pip install --upgrade --force-reinstall --no-cache-dir KratosHDF5Application==9.3.2
    
    # for all
    python3.10 -m pip install --upgrade --force-reinstall --no-cache-dir KratosMultiphysics-all==9.3.0
    
    I get the error when importing KratosHDF5Application, an ImportError: DLL load failed, specified module could not be found.
    
"""

import KratosMultiphysics
from KratosMultiphysics.StructuralMechanicsApplication import *
import KratosMultiphysics.HDF5Application as KratosHDF5
#from KratosMultiphysics.HDF5Application.xdmf_utils import WriteMultifileTemporalAnalysisToXdmf
import os
import json

######################################
# Kratos ModelPart functionalities


def ReadModelPart(mdpa_file_name, model_part_name, materials_file_name=""):
    '''
    Read and return a ModelPart from a mdpa file
    '''
    if mdpa_file_name.endswith('.mdpa'):
        mdpa_file_name = mdpa_file_name[:-5]
    model = KratosMultiphysics.Model()
    model_part = model.CreateModelPart(model_part_name)
    # We reorder because otherwise the numbering might be screwed up when we combine the ModelParts later
    KratosMultiphysics.ReorderConsecutiveModelPartIO(
        mdpa_file_name, KratosMultiphysics.IO.SKIP_TIMER).ReadModelPart(model_part)

    if materials_file_name != "":
        # in case a materials-file is to be combined, it is read and saved as a string
        # for this the ProcessInfo is used => bcs it is shared among (Sub-)ModelParts
        with open(materials_file_name, 'r') as materials_file:
            materials_string = json.dumps(json.load(materials_file))
        model_part.ProcessInfo[KratosMultiphysics.IDENTIFIER] = materials_string
        model_part[KratosMultiphysics.IDENTIFIER] = materials_string

    __RemoveAuxFiles()
    return model_part


def __RemoveAuxFiles():
    '''
    Removes auxiliary files from the directory
    '''
    current_path = os.getcwd()
    files = os.listdir(current_path)
    for file in files:
        if file.endswith(".time") or file.endswith(".lst"):
            os.remove(os.path.join(current_path, file))

######################################
# Kratos H5 functionalities


def WriteH5(file_name, model_part):
    h5_file = __GetHDF5File(file_name, "truncate")
    __OutputModelPartToHDF5(model_part, h5_file)
    __OutputNodalResultsToHDF5(model_part, h5_file, [
                               KratosMultiphysics.AUX_INDEX], is_historical=False)
    del h5_file
    
    # NOTE: has currently a bug, it is not needed
    #WriteMultifileTemporalAnalysisToXdmf(
        #file_name, "/ModelData", "/ResultsData")


def __GetHDF5File(hdf5_file_name, file_access_mode):
    if (KratosHDF5 is None):
        raise Exception(
            "Please compile and install the HDF5 application first.")

    hdf5_file_settings = KratosMultiphysics.Parameters("""{
        "file_name"       : "",
        "file_access_mode": "read_only"
    }""")
    hdf5_file_settings["file_name"].SetString(hdf5_file_name)
    hdf5_file_settings["file_access_mode"].SetString(file_access_mode)
    return KratosHDF5.HDF5FileSerial(hdf5_file_settings)


def __OutputModelPartToHDF5(model_part, hdf5_file):
    if (KratosHDF5 is None):
        raise Exception(
            "Please compile and install the HDF5 application first.")

    KratosHDF5.HDF5ModelPartIO(
        hdf5_file, "/ModelData").WriteModelPart(model_part)


def __OutputNodalResultsToHDF5(model_part, hdf5_file, list_of_variables, is_historical=True, step=0):
    if (KratosHDF5 is None):
        raise Exception(
            "Please compile and install the HDF5 application first.")

    hdf5_output_parameters = KratosMultiphysics.Parameters("""
    {
        "prefix": "/ResultsData",
        "list_of_variables":[]
    }""")
    hdf5_output_parameters["list_of_variables"].SetStringArray(
        __GetListOfVariableNames(list_of_variables))

    if is_historical:
        nodal_io = KratosHDF5.HDF5NodalSolutionStepDataIO(
            hdf5_output_parameters,
            hdf5_file)
        nodal_io.WriteNodalResults(model_part, step)
    else:
        nodal_io = KratosHDF5.HDF5NodalDataValueIO(
            hdf5_output_parameters,
            hdf5_file)
        nodal_io.WriteNodalResults(model_part.Nodes)


def __GetListOfVariableNames(list_of_variables):
    list_of_variable_names = []
    for var in list_of_variables:
        if isinstance(var, str):
            list_of_variable_names.append(var)
        else:
            list_of_variable_names.append(var.Name())
    return list_of_variable_names

