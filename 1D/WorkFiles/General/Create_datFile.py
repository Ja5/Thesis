#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from shutil import copyfile
import os

def Modify_datFile(find, replace, datFile):
    os.system('sed -i "s/^""' + find + '"".*$/""' +
              replace + '""/g" "' + datFile + '"')


def Modify_datFileTestParameters(AlgCoupling, Strategy, Scheme, Model, ElementType, Nt, Nx, L, path_datFile):
    # Adjusting headerFile according to parameters
    MAXTIME = 1190.47619048  #t_f = L^2/D
    
    TIMESTEP = MAXTIME/Nt
    # Mesh parameters
    find = '\/\/ELEMENTS'
    replace = '\/\/ELEMENTS    			' + str(Nx)
    Modify_datFile(find, replace, path_datFile)
    if (ElementType == 'LINE2'):
        Nodes = Nx + 1
    elif (ElementType == 'LINE3'):
        Nodes = 2 * Nx + 1
    else:
        print(NotImplementedError)
    find = '\/\/NODES'
    replace = '\/\/NODES       			' + str(Nodes)
    Modify_datFile(find, replace, path_datFile)
    # Time paramters
    find = 'MAXTIME'
    replace = 'MAXTIME                         '+ str(MAXTIME) +'		\/\/ approx L^2\/D '
    Modify_datFile(find, replace, path_datFile)
    find = 'NUMSTEP'
    replace = 'NUMSTEP                         ' + str(Nt)
    Modify_datFile(find, replace, path_datFile)
    find = 'TIMESTEP'
    replace = 'TIMESTEP                        ' + str(TIMESTEP)
    Modify_datFile(find, replace, path_datFile)
    find = 'MAT 1 MAT_variational_chemicaldiffusion'
    replace = 'MAT 1 MAT_variational_chemicaldiffusion DIFFUSIVITY 8.4e-10 REFMU -190000.0 REFC 26.496 REFTEMP 298.15 GASCON 8.314 MODEL ' + Model
    Modify_datFile(find, replace, path_datFile)

    # Numerical strategy parameters
    if (Scheme == 'SI'):
        find = 'SEMIMPLICITFUNCTIONAL'
        replace = 'SEMIMPLICITFUNCTIONAL		Yes'
        Modify_datFile(find, replace, path_datFile)

    if (AlgCoupling != 'Mono'):
        print "Not coded yet part with preconditioners"


def Create_datFile1D(ElementType, Elements, L, headerPath, fileName):
    # Needed parameters

    # cwd = os.getcwd()  # Gets current directory
    #headerPath = cwd + '/../../BaseFiles/' + headerFile
    #fileName = cwd + '/../datFiles/' + datFile

    if (ElementType == 'LINE2'):  # In general Nodes = (degree element polynomial)*Elements +1
        Nodes = Elements + 1
    elif (ElementType == 'LINE3'):
        Nodes = 2 * Elements + 1

    # Mesh construction
    x = np.linspace(0, L, Nodes)

    # Creates dat file from headerFile (without Mesh)
    copyfile(headerPath, fileName)

    # Output Mesh to file
    with open(fileName, 'a') as myfile:
        StrInFile = '//Elements = ' + str(Elements)
        myfile.write(StrInFile + '\n')
        StrInFile = '//Nodes = ' + str(Nodes)
        myfile.write(StrInFile + '\n')
        StrInFile = '-----------------------------------------------DESIGN DESCRIPTION'
        myfile.write(StrInFile + '\n')
        StrInFile = 'NDPOINT                         2'
        myfile.write(StrInFile + '\n')
        StrInFile = '----------------------------------------------DESIGN POINT DIRICH CONDITIONS'
        myfile.write(StrInFile + '\n')
        StrInFile = 'DPOINT                          1'
        myfile.write(StrInFile + '\n')
        StrInFile = 'E 1 - NUMDOF 2 ONOFF 1 1 VAL 1.0 1.0 FUNCT 2 2'
        myfile.write(StrInFile + '\n')
        StrInFile = '---------------------------------------------DESIGN POINT NEUMANN CONDITIONS'
        myfile.write(StrInFile + '\n')
        StrInFile = 'DPOINT                          1'
        myfile.write(StrInFile + '\n')
        StrInFile = 'E 2 - NUMDOF 2 ONOFF 0 1 VAL 0 1.0 FUNCT 0 3 Live Mid'
        myfile.write(StrInFile + '\n')
        StrInFile = '-----------------------------------------------DNODE-NODE TOPOLOGY'
        myfile.write(StrInFile + '\n')
        if (ElementType == 'LINE2'):
            StrInFile = 'NODE\t' + str(Nodes) + ' DNODE 1'
        elif(ElementType == 'LINE3'):
            StrInFile = 'NODE\t' + str(Nodes - 1) + ' DNODE 1'
        myfile.write(StrInFile + '\n')
        StrInFile = 'NODE\t1 DNODE 2'
        myfile.write(StrInFile + '\n')
        if (ElementType == 'LINE2'):
            StrInFile = '-----------------------------------------------------------------NODE COORDS'
            myfile.write(StrInFile + '\n')
            for node_idx, x_node in enumerate(x, start=1):
                myfile.write('NODE\t' + str(node_idx) + ' COORD ' + "%1.15e" %
                             (x_node) + ' ' + "%1.15e" % (0) + ' ' + "%1.15e" % (0) + '\n')
            StrInFile = '-----------------------------------------------------------------TRANSPORT ELEMENTS'
            myfile.write(StrInFile + '\n')
            for ele in range(1, Elements + 1):
                myfile.write(str(ele) + ' TRANSP ' + ElementType + '  ' + str(ele) +
                             ' ' + str(ele + 1) + '    MAT 1 TYPE VariationalDiffusion' + '\n')
        elif (ElementType == 'LINE3'):
            StrInFile = '-----------------------------------------------------------------NODE COORDS'
            myfile.write(StrInFile + '\n')
            myfile.write('NODE\t1' + ' COORD ' + "%1.15e" % (x[0]) +
                         ' ' + "%1.15e" % (0) + ' ' + "%1.15e" % (0) + '\n')
            for ele in range(0, Elements):
                myfile.write('NODE\t' + str(2 + 2 * ele) + ' COORD ' + "%1.15e" %
                             (x[2 + 2 * ele]) + ' ' + "%1.15e" % (0) + ' ' + "%1.15e" % (0) + '\n')
                myfile.write('NODE\t' + str(3 + 2 * ele) + ' COORD ' + "%1.15e" %
                             (x[1 + 2 * ele]) + ' ' + "%1.15e" % (0) + ' ' + "%1.15e" % (0) + '\n')
            StrInFile = '-----------------------------------------------------------------TRANSPORT ELEMENTS'
            myfile.write(StrInFile + '\n')
            myfile.write(str(1) + ' TRANSP ' + ElementType + '  1 2 3' +
                         '    MAT 1 TYPE VariationalDiffusion' + '\n')
            for ele in range(1, Elements):
                myfile.write(str(ele + 1) + ' TRANSP ' + ElementType + '  ' + str(2 * ele) +
                             ' ' + str(2 * ele + 2) + ' ' + str(2 * ele + 3) + '    MAT 1 TYPE VariationalDiffusion' + '\n')
        StrInFile = '-------------------------------------------------------------------------END'
        myfile.write(StrInFile)






# # ------------------------------------------------------------------
# # ------------------------------------------------------------------
# # ----------                  MAIN CODE       ---------------------
# # ------------------------------------------------------------------
# # ------------------------------------------------------------------

# import os
# cwd = os.getcwd()

# print cwd

# # # Parameters for mesh
# # ElementType = 'LINE2'  # 'LINE2'
# # Elements = 2
# # L = 1e-3
# # LeftNodeBC = 'N'  # Neumann ---- useless
# # RightNodeBC = 'D'  # Dirichlet  ---- still useless my friend

# # headerFile = 'test.txt'

# # Nx_list = [2, 4]

# # # def Generate files for Min Nt
# # for Nx in Nx_list:
# #     # ModifyHeader()
# #     InsertMesh1D('LINE2', Nx, L, headerFile)
# #     # ModifyHeader
# #     InsertMesh1D('LINE3', Nx, L, headerFile)
# #     # Generate numerical solution for reference

# # # Call Setup Alex

# # #InsertMesh(ElementType, Elements, L, headerFile)
