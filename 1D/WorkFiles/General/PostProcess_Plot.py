import os
import numpy as np
import matplotlib.pyplot as plt

# Extracts the error from FileName at the desired time tn


def ReadError_tn(fileName, tn):
    error_tn = []
    with open(fileName, 'r') as f:
        f.readline()                        # Go over title
        f.readline()                        # Go over initial time
        line = f.readline()
        error_tn.append(line.split()[1])    # Gets time step
        while True:
            line = f.readline()
            if not line:
                print 'ERROR: Time ' + str(tn) + '  not found in ' + fileName
                error_tn = -1
                break
            elif str(tn) == line.split()[1]:  # Gets values at tn
                error_tn.extend(line.split()[2:])
                break
        return error_tn

# Creates ErrorFile (curve) for a given BaseName and time tn, according to a specific TestType.
# IMPORTANT: Be sure Nx_list and Nt_list are in accordance the TestType


def CreateFile_Errortn(baseName, Nx_list, tn, Nt_list, TestType):
    fileError_tn = os.getcwd() + '/../../Output/Tests/' + TestType + \
        '_Errortn' + str(tn) + '_' + baseName + '.txt'
    with open(fileError_tn, "w") as output:
        output.write(
            'Nt | dt | Concentrations Errors | Chem Potential Errors' + '\n')

    # Iterate through all time steps
    for i, Nt in enumerate(Nt_list):
        fileName = os.getcwd() + '/../../Output/Results/' + baseName + '_Nx' + \
            str(Nx_list[i]) + '_Nt' + str(Nt) + '.relerror'
        errors = ReadError_tn(fileName, tn)
        with open(fileError_tn, 'a') as f:
            f.write(str(Nt) + ' ' + str(errors).translate(None, "[]',") + '\n')
    return fileError_tn

# Reads file generated with CreateFile_Errortn and generates plot with color col, and legend tn


def FileErrortn2Plot(fileName, tn, col):
    # -------------------------------------Read File
    import csv
    from string import maketrans   # Required to call maketrans function.
    Ntx = []
    dtx = []
    errorC = []
    errorMu = []
    baseName = fileName.split('/')[-1]
    with open(fileName, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            Ntx.append(row[0])
            dtx.append(row[1])
            errorC.append(row[2])
            errorMu.append(row[3])
    # -------------------------------------Draw Plot
    # To use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig = plt.gcf()

    ax = plt.subplot(121)
    plt.xlabel(r'\textbf{Time Step: $\Delta t (s)$}')
    plt.ylabel(r'$E_{c}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltC, = plt.loglog(dtx, errorC, label='tn=' + str(tn))
    pltC.set_color(col)
    plt.legend(loc=0, shadow=True,
               title=baseName[30:53].translate(maketrans("_", "-")))

    # Error at final time
    if tn == 1190.48:
        ComputeErrorSlope(baseName)
        PlotSlopes(baseName, fig, ax, 0)

    ax = plt.subplot(122)
    plt.xlabel(r'\textbf{Time Step}: $\Delta t (s)$')
    plt.ylabel(r'$E_{\mu}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltMu, = plt.loglog(dtx, errorMu,  label='tn=' + str(tn))
    pltMu.set_color(col)
    plt.legend(loc=0, shadow=True,
               title=baseName[30:53].translate(maketrans("_", "-")))

    if tn == 1190.48:
        ComputeErrorSlope(baseName)
        PlotSlopes(baseName, fig, ax, 1)

    # Make room for the ridiculously large title.label on subplot
    plt.subplots_adjust(wspace=0.3)

    return 1


def FileErrortf2Plot(fileName, tn, col):
    # -------------------------------------Read File
    import csv
    from string import maketrans   # Required to call maketrans function.
    Ntx = []
    dtx = []
    errorC = []
    errorMu = []
    baseName = fileName.split('/')[-1]
    with open(fileName, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            Ntx.append(row[0])
            dtx.append(row[1])
            errorC.append(row[2])
            errorMu.append(row[3])
    # -------------------------------------Draw Plot
    # To use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig = plt.gcf()

    ax = plt.subplot(121)
    plt.xlabel(r'\textbf{Time Step: $\Delta t (s)$}')
    plt.ylabel(r'$E_{c}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltC, = plt.loglog(
        dtx, errorC, col, label=baseName[30:53].translate(maketrans("_", "-")))
 #   pltC.set_color(col)
    plt.legend(loc=0, shadow=True,
               title='tn =' + str(tn))

    # Error at final time
    if 'LINE2' in fileName:
        ComputeErrorSlope(baseName)
        PlotSlopes(baseName, fig, ax, 0)

    ax = plt.subplot(122)
    plt.xlabel(r'\textbf{Time Step}: $\Delta t (s)$')
    plt.ylabel(r'$E_{\mu}(t_n,Nx)$')
    plt.title(r'\textbf{Relative Error Nx=512}')
    pltMu, = plt.loglog(dtx, errorMu, col,
                        label=baseName[30:53].translate(maketrans("_", "-")))
#    pltMu.set_color(col)
    plt.legend(loc=0, shadow=True,
               title='tn=' + str(tn))

    if 'LINE2' in fileName:
        ComputeErrorSlope(baseName)
        PlotSlopes(baseName, fig, ax, 1)

    # Make room for the ridiculously large title.label on subplot
    plt.subplots_adjust(wspace=0.3)

    return 1


# Plots all curves, for all times tn, for a given TestType and BaseName


def Plot_AllTest_tn(baseName, Nx_list, tn, Nt_list, TestType):
    Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

    fig = plt.figure()

    for i, tn in enumerate([297.619, 446.429, 595.238, 744.048, 892.857, 1041.67, 1190.48]):
        fileName = CreateFile_Errortn(baseName, Nx_list, tn, Nt_list, TestType)
        FileErrortn2Plot(fileName, tn, Color_list[i])
        # ComputeErrorSlope(fileName)

    # plt.show()

    # Saving figure
    figName = os.getcwd() + '/../../Output/Plots/' + TestType + '_All_' + baseName
    fig.savefig(figName + '.pdf', bbox_inches='tight')
    # To later use in latex do...
    # fig.savefig(figName+'.pgf', bbox_inches='tight')
    # ......on latex add/ $ usepackage{pgfplots}

    plt.close(fig)

# Does the complete plot for a given time step tn TestType given an ErrorType


def Tests2Plot_tf(TestType, AlgCoupling, Strategy, Scheme, ElementType, Model, Nx_list, Nt_list, tn):
    Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    i = 0
    fig = plt.gcf()
    plt.close(fig)
    for AlgC in ['Mono']:  # AlgCoupling:
        for Strg in ['NM']:  # Strategy:
            if AlgC != 'Mono' and (Strg != 'NM' or Strg != 'AMG'):
                break
            for Schm in Scheme:
                for ElemTyp in ElementType:
                    for Mod in ['Fickean']:  # Model:
                        baseName = AlgC + Strg + '_' + Schm + '_' + Mod + '_' + ElemTyp
                        lineFormat = Color_list[i]
                        if ElemTyp == 'LINE3':
                            lineFormat = '+-.' + lineFormat
                        fileError = CreateFile_Errortn(
                            baseName, Nx_list, tn, Nt_list, TestType)
                        print fileError
                        FileErrortf2Plot(fileError, tn, lineFormat)

                        # if ElemTyp == 'LINE3':
                        #     PlotSlopes(fileName)
                        i = i + 1
    # plt.show()
    fig = plt.gcf()
    # Saving figure
    figName = os.getcwd() + '/../../Output/Plots/' + TestType + '_All_' + baseName
    fig.savefig(figName + '.pdf', bbox_inches='tight')
    # To later use in latex do...
    #fig.savefig(figName+'.pgf', bbox_inches='tight')
    # ......on latex add/ $ usepackage{pgfplots}

    return 1


# Computes the error slopes in a filefrom fileName and saves them into '.../Test/Slope_fileName'


def ComputeErrorSlope(fileName):
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
            Ntx.append(float(row[0]))
            dtx.append(float(row[1]))
            errorC.append(float(row[2]))
            errorMu.append(float(row[3].translate(None, ";")))
    # -------------------------------------Computations
    SlopefileName = os.getcwd() + '/../../Output/Tests/' + 'Slope_' + fileName
    import math
    with open(SlopefileName, 'w') as f:
        f.write('PosX |  PosY | Slope Concentration | Slope Chemical Potential \n')
        for i, dt in enumerate(dtx[:-1]):
            SlopeC = (abs(math.log(errorC[i + 1]) - math.log(errorC[i]))
                      ) / (abs(math.log(dtx[i + 1]) - math.log(dt)))
            SlopeMu = (abs(math.log(errorMu[i + 1]) - math.log(errorMu[i]))) / (
                abs(math.log(dtx[i + 1]) - math.log(dt)))
            f.write(str((dt + dtx[i + 1]) / 2) + ' ' + str((errorC[i] + errorC[i + 1]) / 2) + ' ' + str(
                (errorMu[i] + errorMu[i + 1]) / 2) + ' ' + str(SlopeC) + ' ' + str(SlopeMu) + '\n')
    return SlopefileName

# Plots slopes already saved from ComputeErrorSlope from fileName


def PlotSlopes(fileName, fig, ax, index):
    filePath = os.getcwd() + '/../../Output/Tests/' + 'Slope_' + fileName
    # -------------------------------------Read File
    import csv
    import math
    # fig = plt.gcf()
    # Axes = plt.gca()
    with open(filePath, 'r') as f:
        next(f)
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            numVar = (len(row) - 1) / 2
            ax.text(row[0], row[1 + index], row[1 + numVar + index][:4],
                    transform=ax.transData, va='top', ha='left', alpha=0.5)
    return 1

# Plots from Test Results -> locates the files form Tests


def FileTest2Plot(fileName, baseName, col):
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
            Ntx.append(row[0])
            dtx.append(row[1])
            errorC.append(row[2])
            errorMu.append(row[3].translate(None, ";"))
    ComputeErrorSlope(fileName)
    # -------------------------------------Draw Plot
    # To use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    from string import maketrans   # Required to call maketrans function.
    baseNameTranslated = baseName.translate(maketrans("_", "-"))

    fig = plt.figure(1)
    fig.suptitle(r'\textbf{Mean Error per Time Step (Nx=512)', fontsize=16)

    ax = fig.add_subplot(121)

    plt.xlabel(r'\textbf{Time Step } $\Delta t (s)$')
    plt.ylabel(r'$\tilde{E}_{c}(Nx)$')
    plt.title(r'\textbf{Concentration}')
    pltC, = plt.loglog(dtx, errorC, col, label=baseNameTranslated)
    # pltC.set_color(col)
    plt.legend(loc=4, borderaxespad=0.)
    if 'LINE3' in fileName:
        PlotSlopes(fileName, fig, ax, 0)

    ax = fig.add_subplot(122)
    # Make room for the ridiculously large title.label on subplot
    plt.subplots_adjust(wspace=0.4)
    plt.xlabel(r'\textbf{Time Step } $\Delta t (s)$')
    plt.ylabel(r'$\tilde{E}_{\mu}(Nx)$')
    plt.title(r'\textbf{Chemical Potential}')
    pltMu, = plt.loglog(dtx, errorMu, col, label=baseNameTranslated)
    # pltMu.set_color(col)
    plt.legend(loc=4, borderaxespad=0.)
    if 'LINE3' in fileName:
        PlotSlopes(fileName, fig, ax, 1)

    return 1

# Does the complete plot for a TestType given an ErrorType


def Tests2Plot(TestType, ErrorType, AlgCoupling, Strategy, Scheme, ElementType, Model):
    Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    i = 0
    fig = plt.gcf()
    plt.close(fig)
    for AlgC in ['Mono']:  # AlgCoupling:
        for Strg in ['NM']:  # Strategy:
            if AlgC != 'Mono' and (Strg != 'NM' or Strg != 'AMG'):
                break
            for Schm in ['SI']:  # Scheme:
                for ElemTyp in ElementType:
                    for Mod in ['Linear']:  # Model:
                        baseName = AlgC + Strg + '_' + Schm + '_' + Mod + '_' + ElemTyp
                        fileName = TestType + '_' + ErrorType + '_' + baseName + '.txt'
                        lineFormat = Color_list[i]
                        if ElemTyp == 'LINE3':
                            lineFormat = '+-.' + lineFormat
                        FileTest2Plot(fileName, baseName, lineFormat)
                        # if ElemTyp == 'LINE3':
                        #     PlotSlopes(fileName)
                        i = i + 1
    # plt.show()
    fig = plt.gcf()
    # Saving figure
    figName = os.getcwd() + '/../../Output/Plots/' + TestType + '_' + ErrorType
    fig.savefig(figName + '.pdf', bbox_inches='tight')
    # To later use in latex do...
    #fig.savefig(figName+'.pgf', bbox_inches='tight')
    # ......on latex add/ $ usepackage{pgfplots}

    return 1

# Creates the plots for all Test using all errortypes


def Plot_AllTest_ErrorType():
    TestTypes = ['OmegaFix_Nx512', 'RatioNxNt1']
    ErrorTypes = ['L2Error', 'TimeInt']
    for TestType in TestTypes:
        for ErrorType in ErrorTypes:
            Tests2Plot(TestType, ErrorType, AlgCoupling,
                       Strategy, Scheme, ElementType, Model)
    return 1

# --------------------------------------------------------------------------------
# ----------------------------------    MAIN    ----------------------------------
# --------------------------------------------------------------------------------


baseName = 'MonoNM_FI_Fickean_LINE2'
tn = 1190.48
samplePoints = 10
Nt_list_float = pow(2, np.linspace(1 + 2, samplePoints + 2, samplePoints))
Nt_list = [int(i) for i in Nt_list_float]


# TestType = 'RatioFix_1'
# ratio = 1
# Nx_list = ratio*Nt_list;

Nx_list = [512, 512, 512, 512, 512, 512, 512, 512, 512, 512]

from Tests import ReadTestParameters
AlgCoupling, Strategy, Scheme, ElementType, Model = ReadTestParameters(
    'TestParameters.dat')

plt.style.use('mythesis')

Color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
col = Color_list[1]
TestType = 'RatioNxNt1'
Nx_list = Nt_list

# Plots from baseName all the matching lines between Nt_list
# Plot_AllTest_tn(baseName, Nx_list, tn, Nt_list, TestType)

# Plot TestType convergence plot at time tn
Tests2Plot_tf(TestType, AlgCoupling, Strategy, Scheme,
              ElementType, Model, Nx_list, Nt_list, tn)

quit()
# Creates the plots for all Test using all errortypes
Plot_AllTest_ErrorType()


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
