def ReadTestParameters(fileName):
    with open(fileName, 'r') as f:
        for line in f:
            if 'AlgCoupling' in line:
                # Remove brackets and '', remove \n, split from =
                temp = line.translate(None, "[]' ").strip().split('=', 1)[1]
                AlgCoupling = temp.split(',')
            elif 'Strategy' in line:
                temp = line.translate(None, "[]' ").strip().split('=', 1)[1]
                Strategy = temp.split(',')
            elif 'Scheme' in line:
                temp = line.translate(None, "[]' ").strip().split('=', 1)[1]
                Scheme = temp.split(',')
            elif 'ElementType' in line:
                temp = line.translate(None, "[]' ").strip().split('=', 1)[1]
                ElementType = temp.split(',')
            elif 'Model' in line:
                temp = line.translate(None, "[]' ").strip().split('=', 1)[1]
                Model = temp.split(',')
    return [AlgCoupling, Strategy, Scheme, ElementType, Model]

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ----------                  MAIN CODE       ---------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------


import os
import math
import numpy as np
from Tests import Omega_hFix
from Tests import RatioNxNt_Fix
from Tests import TestFile


# Files & Directories
home = os.path.expanduser('~')
dir_baci = home + '/workspace/build-release'

cwd = os.getcwd()
dir_Results = cwd + '/../../Output/Results'
dir_logFiles = cwd + '/../../Output/logFiles'
dir_datFiles = cwd + '/../datFiles'
dir_Plots = cwd + '/../../Output/Plots'


#---------------------PARAMETERS
L = 1e-3

AlgCoupling, Strategy, Scheme, ElementType, Model = ReadTestParameters(
    'TestParameters.dat')

samplePoints = 1
Nt_list_float = pow(2, np.linspace(1 + 2, samplePoints + 2, samplePoints))
Nt_list = [int(i) for i in Nt_list_float]

#---------------------- SPECIFICS
ErrorType = 'L2Error/TimeInt'
Action = 'SRP'  # Setup/Run/PostProcess
Nx = 2**9

#********************************************Compute numerical reference solution

# Condition for maximum time step without spurious oscillaitons
#-----
powNt = math.floor(math.log(6 * Nx**2, 2))
Nt = int(2**powNt)
#-----

headerFile = 'InitialDiscontinuity.head'
path_header = cwd + '/../../BaseFiles/' + headerFile

# To output only the needed results for reference
ResemblanceRatio = Nt/(samplePoints + 2)
find = 'RESULTSEVRY'
replace = 'RESULTSEVRY                     ' + str(ResemblanceRatio)
from Create_datFile import Modify_datFile
Modify_datFile(find, replace, path_header)

for Schm in Scheme:
    for EleTyp in ElementType:
        for Mod in Model:
            print TestFile('Mono', 'NM', Schm, Mod, EleTyp, Nx, Nt, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, 'SR', '')

# Setting for normal test
ResemblanceRatio = Nt/(samplePoints + 2)
find = 'RESULTSEVRY'
replace = 'RESULTSEVRY                     1' 
Modify_datFile(find, replace, path_header)


#********************************************Test1
# Omega_hFix test
Nx = 2**9
# Fix ratio test
ratio = 1
for AlgC in AlgCoupling:
    for Strg in Strategy:
        if AlgC != 'Mono' and (Strg != 'NM' or Strg != 'AMG'):
            break
        if Strg == 'AMG':
            headerFile = 'InitialDiscontinuityAMG.head'
        else:
            headerFile = 'InitialDiscontinuity.head'
        path_header = cwd + '/../../BaseFiles/' + headerFile
        for Schm in Scheme:
            for EleTyp in ElementType:
                for Mod in Model:
                    print AlgC + '_' + Strg + '_' + Schm + '_' + Mod + '_' + EleTyp + '_Nx' + str(Nx) + '_Nt' + str(Nt)
                    #Omega_hFix(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)
                    #RatioNxNt_Fix(AlgCoupling, Strategy, Scheme, Model, ElementType, ratio, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)
