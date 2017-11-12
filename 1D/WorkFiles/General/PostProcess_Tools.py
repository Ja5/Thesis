import os
import math
import numpy as np
import csv


# Read element and its nodes from Baci

def SaveListIntoFile(fileName, listName):
    with open(fileName, "a") as output:
        #output.write('Numsteps| dt | Concentrations Errors | Chem Potential Errors' + '\n')
        for errorTest in listName:
            output.write(str(errorTest).translate(None, "()#,") + ';\n')


def GetNodes_datFile(datFile):
    with open(datFile, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                print 'ERROR: Number of nodes not found in ' + datFile
                return -1
                break
            if 'Nodes' in line:
                for nodes in line.split():
                    if nodes.isdigit():
                        return int(nodes)
                        break


def ReadNodeError_relErrorFile(fileName, node):
    with open(fileName, 'r') as f:
        for _ in xrange(node):
            next(f)		# Title errors
        line = next(f)
        if not line:
            print 'Node (' + str(node) + ') not found in ' + fileName
            return -1
        dataStr = line.split()
        return float(dataStr[-2]), float(dataStr[-1])


# Rewritten below since next(f) creates StopItertion
def ReadTempNodeError_relErrorFileXXX(fileName, timeStep):
    with open(fileName, 'r') as f:
        for _ in xrange(timeStep + 1):   	# +1 due to title
            line = next(f)
        line = next(f)
        if not line:
            print 'WARNING: File ended before reaching the time step: ' + str(timeStep) + '\n File:' + fileName
            return 0, 0
        dataStr = line.split()
        return float(dataStr[-2]), float(dataStr[-1])


def ReadTempNodeError_relErrorFile(fileName, timeStep):
    with open(fileName, 'r') as f:
        for i, line in enumerate(f):   	# +1 due to title
            if i <= timeStep:
                continue
            if not line:
                print 'WARNING: File ended before reaching the time step: ' + str(timeStep) + '\n File:' + fileName
                return 0, 0
            dataStr = line.split()
            return float(dataStr[-2]), float(dataStr[-1])
        print 'WARNING: File ended before reaching the time step: ' + str(timeStep) + '\n File:' + fileName
        return 'NaN'


def GetNodeCoordFrom_datFile(datFile, node):
    with open(datFile, 'r') as f:
        while True:
            line = f.readline()
            if 'NODE COORDS' in line:
                for _ in xrange(node - 1):
                    line = f.readline()
                line = f.readline()
                coords = line.split()
                break
            if not line:
                break
    return coords[3:6]


def GetFrom_datFile(datFile, String):
    with open(datFile, 'r') as f:
        while True:
            line = f.readline()
            if String in line:
                tmp = line.split()
                extract = tmp[-1]
                break
            if not line:
                print 'ERROR: ' + String + ' not found in file :\n' + datFile
                extract = -1
                break
    return extract

# Computes L2 Error per time step


def L2Error_relErrorFile(datFile, resultsFile):
    ErrorC = 0
    ErrorMu = 0
    numstep = int(GetFrom_datFile(datFile, 'NUMSTEP'))
    dt = float(GetFrom_datFile(datFile, 'TIMESTEP'))
    if numstep == -1:
        print 'ERROR: NUMSTEP not found in call to: GetFrom_datFile \n From file : ' + datFile
    for timeStep in xrange(1, numstep + 1):
        tempError = ReadTempNodeError_relErrorFile(resultsFile, timeStep)
        if tempError == 'NaN':
            print 'ERROR: While substracting data from: ReadTempNodeError_relErrorFile\n' + 'file: ' + resultsFile
            return 'NaN', 'NaN'
        ErrorC = tempError[0] + ErrorC
        ErrorMu = tempError[1] + ErrorMu
    return numstep, dt, ErrorC / numstep, ErrorMu / numstep

# Computes L2 Time integration Error


def TimeInt_relErrorFile(datFile, resultsFile):
    ErrorC = 0
    ErrorMu = 0
    numstep = int(GetFrom_datFile(datFile, 'NUMSTEP'))
    dt = float(GetFrom_datFile(datFile, 'TIMESTEP'))
    tempError = []
    if numstep == -1:
        print 'ERROR: NUMSTEP not found in call to: GetFrom_datFile \n From file : ' + datFile

    for timeStep in xrange(1, numstep + 1):
        tempError.append(ReadTempNodeError_relErrorFile(resultsFile, timeStep))

    ErrorC = np.trapz(zip(*tempError)[0], dx=dt)
    ErrorMu = np.trapz(zip(*tempError)[1], dx=dt)

    return numstep, dt, ErrorC, ErrorMu


def IntegrateFEMFrom_datFile(datFile):
    with open(path_datFile, 'r') as f:
        while True:
            line = f.readline()
            if 'TRANSPORT ELEMENTS' in line:
                while True:
                    line = f.readline()

                    if not line:
                        print 'Not END of BACI dat-file found'
                        break
                    elif 'END' in line:
                        break
                    else:
                        description = line.split()
                        if (description[2] == 'LINE2'):
                            Nodes = description[3:5]
                        elif (description[2] == 'LINE3'):
                            Nodes = description[3:6]
                        # print 'Element = ' + str(description[0]) + '\n'
                        for node in Nodes:
                            coords = GetNodeCoordFrom_datFile(
                                path_datFile, int(node))
                            print 'GetQuadrature points before  nodes loop andhere: Read result and interpolate, save in a resultFile to later use ReadNodeError_relErrorFile'
                            # print '\t xCoord = ' + str(coords[0]) + '\n'

            if not line:
                break


# dO GENERAL FOR RELATIVE ERRORS
def PlotError(ErrorfileName, Nt_list):
    with open('./../../Output/Tests/Convergence_Omega_hFix_Nx10.txt', 'r') as f:
        ErrorC = []
        ErrorMu = []
        for i, line in enumerate(f):
            if i == 0:
                continue
            dataStr = line.split()
            if dataStr[0] != "'NaN'":
                ErrorC.append(float(dataStr[0]))
                ErrorMu.append(float(dataStr[1]))
    # print ErrorC
    # print ErrorMu
    plt.subplot(1, 2, 1)
    plt.loglog(Nt_list, ErrorC)
    plt.subplot(1, 2, 2)
    plt.loglog(Nt_list, ErrorMu)
    plt.show()
# # ------------------------------------------------------------------
# # ------------------------------------------------------------------
# # ----------                  MAIN CODE       ---------------------
# # ------------------------------------------------------------------
# # ------------------------------------------------------------------


#cwd = os.getcwd()
#datFile = 'MonoNM_FI_LINE2_Nx4_Nt2.dat'
#path_datFile = cwd + '/../datFiles/' + datFile
#path_resultsFile = cwd + '/EjemploResult.csv'


#resultsFile = path_resultsFile
#datFile = path_datFile
#node = 3

# print ReadTempNodeError_relErrorFile('./../../Output/Results/MonoNM_FI_Fickean_LINE2_Nx10_Nt8.relerror', 8)
# print L2Error_relErrorFile('./../../WorkFiles/datFiles/MonoNM_FI_Fickean_LINE2_Nx10_Nt8.dat', './../../Output/Results/MonoNM_FI_Fickean_LINE2_Nx10_Nt8.relerror')

# print L2Error_relErrorFile(datFile, resultsFile)
# print GetFrom_datFile(datFile, 'TIMESTEP')

# Errors = PostProcess_Omega_hFix(....)
# SaveListIntoFile(fileName,listName):

# print Error

# IntegrateFEMFrom_datFile(path_datFile)
