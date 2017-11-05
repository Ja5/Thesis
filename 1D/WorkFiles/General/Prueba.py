import os
import numpy as np
from Tests import Omega_hFix
from Tests import RatioNxNt_Fix

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ----------                  MAIN CODE       ---------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------


# Files & Directories
headerFile = 'InitialDiscontinuity.head'
#headerFile = 'InitialDiscontinuityAMG.head'  # Remember to add xml file in datFiles folder - Create a funcion in Createdatfile to look for it and send error if not

home = os.path.expanduser('~')
dir_baci = home + '/workspace/build-release'

cwd = os.getcwd()
path_header = cwd + '/../../BaseFiles/' + headerFile
dir_Results = cwd + '/../../Output/Results'
dir_logFiles = cwd + '/../../Output/logFiles'
dir_datFiles = cwd + '/../datFiles'
dir_Plots= cwd + '/../../Output/Plots'

#---------------------PARAMETERS
AlgCoupling = 'Mono'
Strategy = 'NM'
ElementType = 'LINE2'
Scheme = 'FI'
Model = 'Fickean'
L = 1e-3


samplePoints = 3
Nt_list_float = pow(2,np.linspace(1+2,samplePoints+2,samplePoints))
Nt_list = [int(i) for i in Nt_list_float]

#---------------------- SPECIFICS
ErrorType = 'L2Error/TimeInt'
Action = 'SRP'  # Setup/Run/PostProcess
# Omega_hFix test
Nx = 10
# Fix ratio test
ratio = 1

# Test hierarchy
#AlgCoupling + Strategy + '_' + Scheme + '_' + Model + '_' + ElementType 

#********************************************Test1
Omega_hFix(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)

RatioNxNt_Fix(AlgCoupling, Strategy, Scheme, Model, ElementType, ratio, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)

##############################
headerFile = 'InitialDiscontinuityAMG.head'  # Remember to add xml file in datFiles folder - Create a funcion in Createdatfile to look for it and send error if not
path_header = cwd + '/../../BaseFiles/' + headerFile
Strategy = 'AMG'

#********************************************Test1
Omega_hFix(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)

RatioNxNt_Fix(AlgCoupling, Strategy, Scheme, Model, ElementType, ratio, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action)


