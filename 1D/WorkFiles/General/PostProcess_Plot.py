import os
import numpy as np
import matplotlib.pyplot as plt

# Extracts the error from FileName at the desired time tn


def ReadError_tn(fileName, tn):
    with open(fileName, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                print 'ERROR: Time ' + str(tn) + '  not found in ' + fileName
                error_tn = -1
                break
            elif str(tn) == line.split()[1]:
                error_tn = line.split()[2:]
                break
        return error_tn

# Creates ErrorFile (curve) for a given BaseName and time tn, according to a specific TestType


def CreateFile_Errortn(baseName, Nx_list, tn, Nt_list, TestType):
    fileError_tn = os.getcwd() + '/../../Output/Plots/' + TestType + \
        '_Errortn' + str(tn) + '_' + baseName + '.txt'
    with open(fileError_tn, "w") as output:
        output.write(
            'Nt | Concentrations Errors | Chem Potential Errors' + '\n')

    # Iterate through all time steps
    for i, Nt in enumerate(Nt_list):
        fileName = os.getcwd() + '/../../Output/Results/' + baseName + '_Nx' + \
            str(Nx_list[i]) + '_Nt' + str(Nt) + '.relerror'
        errors = ReadError_tn(fileName, tn)
        with open(fileError_tn, 'a') as f:
            f.write(str(Nt) + ' ' + str(errors).translate(None, "[]',") + '\n')
    return 1

# --------------------------------------------------------------------------------
# ----------------------------------    MAIN    ----------------------------------


baseName = 'MonoAMG_FI_Fickean_LINE2'
tn = 1190.48
samplePoints = 10
Nt_list_float = pow(2, np.linspace(1 + 2, samplePoints + 2, samplePoints))
Nt_list = [int(i) for i in Nt_list_float]
TestType = 'RatioFix_1'
Nx_list = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
for tn in [148.81, 297.619, 446.429, 595.238, 744.048, 892.857, 1041.67, 1190.48]:
    CreateFile_Errortn(baseName, Nx_list, tn, Nt_list, TestType)


print 'FIN'


# # ********************************************************************************
# # Example how to plot in matplotlib and export in PDF and PGF using a user pre-defined style
# # ********************************************************************************

# plt.style.use('presentation')

# print(plt.style.available)


# plt.figure()
# plt.subplot(121)

# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title('Histogram of IQ')

# line_up, = plt.plot([1, 2, 3], label='Line 2')
# line_down, = plt.plot([3, 2, 1], label='Line 1')
# plt.legend([line_up, line_down], ['Line Up', 'Line Down'])

# with plt.style.context(('mythesis')):
#     plt.subplot(122)

#     plt.xlabel('Smarts')
#     plt.ylabel('Probability')
#     plt.title('Histogram of IQ')

#     line_up, = plt.plot([1, 2, 3], label='Line 2')
#     line_down, = plt.plot([3, 2, 1], label='Line 1')
#     plt.legend([line_up, line_down], ['Line Up', 'Line Down'])


# plt.show()
