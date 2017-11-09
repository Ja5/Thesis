
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

# Creates ErrorFile (curve) for a given BaseName and time tn, according to a specific TestType.
# IMPORTANT: Be sure Nx_list and Nt_list are in accordance the TestType


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
    return fileError_tn

# Reads file generated with CreateFile_Errortn and generates plot with color col, and legend tn

def FileErrortn2Plot(fileName,tn,col):
    # -------------------------------------Read File
    import csv
    Ntx = []
    errorC = []
    errorMu = []
    with open(fileName, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            Ntx.append( row[0])
            errorC.append(row[1])
            errorMu.append(row[2])
    # -------------------------------------Draw Plot
    # To use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    plt.subplot(121)
    plt.xlabel(r'\textbf{Time Steps}')
    plt.ylabel(r'$E_{c}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltC, = plt.loglog(Ntx, errorC, label='tn='+str(tn))
    pltC.set_color(col)
    plt.legend()

    plt.subplot(122)
    plt.xlabel(r'\textbf{Time Steps}')
    plt.ylabel(r'$E_{\mu}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltMu, = plt.loglog(Ntx,errorMu,  label='tn='+str(tn))
    pltMu.set_color(col)
    plt.legend()
    
    # Make room for the ridiculously large title.label on subplot
    plt.subplots_adjust(wspace=0.3)
    
    return 1

# Plots all curves, for all times tn, for a given TestType and BaseName
def Plot_AllTest_tn(baseName, Nx_list, tn, Nt_list, TestType):
    Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    fig = plt.figure()

    for i,tn in enumerate([297.619, 446.429, 595.238, 744.048, 892.857, 1041.67, 1190.48]):
        fileName = CreateFile_Errortn(baseName, Nx_list, tn, Nt_list, TestType)
        FileErrortn2Plot(fileName,tn,Color_list[i])

    #plt.show()

    # Saving figure
    figName =  os.getcwd() + '/../../Output/Plots/' + TestType + '_All_' + baseName
    fig.savefig(figName+'.pdf', bbox_inches='tight')
    # To later use in latex do...
    #fig.savefig(figName+'.pgf', bbox_inches='tight')
    ##......on latex add/ $ usepackage{pgfplots}

# Plots from Test Results -> locates the files form Tests
def FileTest2Plot(fileName,col):
    filePath = os.getcwd() + '/../../Output/Tests/' + fileName

    # -------------------------------------Read File
    import csv
    Ntx = []
    dtx = []
    errorC = []
    errorMu = []
    with open(filePath, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            Ntx.append( row[0])
            dtx.append(row[1])
            errorC.append(row[2])
            errorMu.append(row[3].translate(None, ";"))
    # -------------------------------------Draw Plot
    # To use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    from string import maketrans   # Required to call maketrans function.
    baseNameTranslated = baseName.translate(maketrans("_","-"))

    fig = plt.figure(1)
    fig.suptitle(r'\textbf{Mean Error per Time Step (Nx=512)', fontsize=16)

    plt.subplot(121)
    plt.xlabel(r'\textbf{Time Step } $\Delta t (s)$')
    plt.ylabel(r'$\tilde{E}_{c}(Nx)$')
    plt.title(r'\textbf{Concentration}')
    pltC, = plt.loglog(dtx, errorC, label=baseNameTranslated)
    pltC.set_color(col)
    plt.legend(loc=4, borderaxespad=0.)

    plt.subplot(122)
    plt.xlabel(r'\textbf{Time Step } $\Delta t (s)$')
    plt.ylabel(r'$\tilde{E}_{\mu}(Nx)$')
    plt.title(r'\textbf{Chemical Potential}')
    pltMu, = plt.loglog(dtx,errorMu,  label=baseNameTranslated)
    pltMu.set_color(col)
    plt.legend(loc=4, borderaxespad=0.)
    # Make room for the ridiculously large title.label on subplot
    plt.subplots_adjust(wspace=0.3)
    
    return 1            
# --------------------------------------------------------------------------------
# ----------------------------------    MAIN    ----------------------------------
# --------------------------------------------------------------------------------

baseName = 'MonoNM_FI_Fickean_LINE2'
tn = 1190.48
samplePoints = 10
Nt_list_float = pow(2, np.linspace(1 + 2, samplePoints + 2, samplePoints))
Nt_list = [int(i) for i in Nt_list_float]


#TestType = 'RatioFix_1'
#ratio = 1
#Nx_list = ratio*Nt_list;

Nx_list = [512, 512, 512, 512, 512, 512, 512, 512, 512, 512]

from Tests import ReadTestParameters
AlgCoupling, Strategy, Scheme, ElementType, Model = ReadTestParameters('TestParameters.dat')


# Plots from baseName all the matching lines between Nt_list
# Plot_AllTest_tn(baseName, Nx_list, tn, Nt_list, TestType)

Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
col = Color_list[1]

plt.style.use('ggplot')


TestType = 'OmegaFix_Nx512'
ErrorType = 'L2Error' #TimeInt
i=0
for AlgC in ['Mono']:#AlgCoupling:
    for Strg in ['NM']:#Strategy:
        if AlgC != 'Mono' and (Strg != 'NM' or Strg != 'AMG'):
            break
        for Schm in ['FI']:#Scheme:
            for ElemTyp in ElementType:
                for Mod in ['Fickean']:#Model:
                    baseName = AlgC + Strg + '_' + Schm + '_' + Mod + '_' + ElemTyp
                    fileName = TestType +'_' + ErrorType +'_' + baseName + '.txt'
                    FileTest2Plot(fileName,Color_list[i])
                    i =i+1
plt.show()
                    
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
