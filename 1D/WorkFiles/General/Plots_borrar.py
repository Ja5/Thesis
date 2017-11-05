# think what to do with relerror files, how to direct them idependet of it is baci created or local

import os

def Omega_hFix(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action):

    print '********************************************************************************************************************************************\n'
    print '****************************************************************Omega_h test****************************************************************\n'
    print '********************************************************************************************************************************************\n'

    for i,Nt in enumerate(Nt_list):

	TestFile(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action,'NxFix'+str(Nx))
 
def RatioNxNt_Fix(AlgCoupling, Strategy, Scheme, Model, ElementType, ratio, Nt_list, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action):

    print '********************************************************************************************************************************************\n'
    print '*************************************************************RatioNxNt_Fix test*************************************************************\n'
    print '********************************************************************************************************************************************\n'

    for i,Nt in enumerate(Nt_list):

	Nx = Nt*ratio
	TestFile(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action, 'RatioNxNt'+str(ratio))

def TestFile(AlgCoupling, Strategy, Scheme, Model, ElementType, Nx, Nt, L, path_header, dir_baci, dir_datFiles, dir_Results, dir_logFiles, dir_Plots, ErrorType, Action,testName):
    baseName = AlgCoupling + Strategy + '_' + Scheme + '_' + Model + '_' + ElementType + '_Nx' + str(Nx) + '_Nt' + str(Nt)
    datFile = baseName + '.dat'
    path_datFile = dir_datFiles + '/' + datFile
    path_Results = dir_Results + '/' + baseName
    path_logFiles = dir_logFiles + '/' + baseName + '.txt'
    path_errorFile = dir_Results + '/' + baseName + '.relerror'

    # Checking/creating datFile
    print '----------------------Checking files for ' + testName + ' test-------------\n'
    if (not os.path.isfile(path_datFile)):

        if 'S' in Action:

            print '----------------------Creating files for ' + testName + ' test-------------\n'
            from Create_datFile import Modify_datFileTestParameters

            from Create_datFile import Create_datFile1D					# in higher dim here goes an if
            Create_datFile1D(ElementType, Nx, L, path_header, path_datFile)

            Modify_datFileTestParameters(AlgCoupling, Strategy, Scheme, Model, ElementType, Nt, Nx, L, path_datFile)
        else:
            print 'ERROR: datFile does not exits. Run Test including setup' + '\n\t' + path_datFile
    else:
        if 'S' in Action:            
            print 'WARNING: The file already exists. It was not generated \n\t' +  path_datFile


    # Running/PostProcessing datFile
    if (os.path.isfile(path_datFile)):
        if 'R' in Action:

            print '----------------------Running files for ' + testName + ' test-------------\n'

            if (not os.path.isfile(path_Results + '_scatra.case')):

                Str = dir_baci + '/baci-release ' + path_datFile + ' ' + path_Results + ' >> ' + path_logFiles
                print '\nRunning baci:\n' +  Str + '\n'
                os.system(Str)

                Str = dir_baci + '/post_drt_ensight ' + ' --file='+ path_Results
                print '\nRunning post_drt_ensight:\n' +  Str  + '\n'
                os.system(Str)

                Str = dir_baci + '/post_processor ' + ' --file='+ path_Results  + ' --filter=vtu --outputtype=ascii'        
                print '\nRunning post_processor:\n' +  Str + '\n'
                os.system(Str)
            else:
                print 'WARNING: The results already exist. Skiping Run Test' + '\n\t' + path_Results + '_scatra.case'

            # Add here the condition to run for the numerical comparison & generating *.relerror file

        if 'P' in Action:
            from PostProcess_Tools import SaveListIntoFile
            baseName_PostProcess = AlgCoupling + Strategy + '_' + Scheme + '_' + Model + '_' + ElementType + '_Nx' + str(Nx)
            print '----------------------Post-processing files for ' + testName + ' test-------------\n'

            if (os.path.isfile(path_errorFile)):

                # Temporal Errors
                if 'L2Error' in ErrorType:		# Add here different type of desired errors to plot
                    from PostProcess_Tools import L2Error_relErrorFile

                    Errors = []
                    Errors.append(L2Error_relErrorFile(path_datFile, path_errorFile))

                    print 'Saving ' + ErrorType + ' results into file:\n' + path_Results + '/../Tests/' + testName + '_' + ErrorType + '_Nx' + str(Nx) + '.txt\n'
                    SaveListIntoFile(dir_Results + '/../Tests/' + testName + '_L2Error' + '_' + baseName_PostProcess + '.txt', Errors)

                    # Generate corresponding plots

                if 'TimeInt' in ErrorType:
                    from PostProcess_Tools import TimeInt_relErrorFile

                    Errors = []
                    Errors.append(TimeInt_relErrorFile(path_datFile, path_errorFile))

                    print 'Saving ' + ErrorType + ' results into file:\n' + path_Results + '/../Tests/' + testName + '_' + ErrorType + '_Nx' + str(Nx) + '.txt\n'
                    SaveListIntoFile(dir_Results + '/../Tests/' + testName + '_TimeInt' + '_' + baseName_PostProcess + '.txt', Errors)

                    # Generate corresponding plots
            else:
                print 'ERROR: The error file for this test does not exist' + '\n\t' + path_errorFile

    else:
        print 'ERROR: The dat file for this test does not exist' + '\n\t' + path_datFile

# think what to do with relerror files, how to direct them idependet of it is baci created or local
def Plottt:
	
	plt.style.use('presentation')
	
	plt.figure()
	plt.subplot(121)

	plt.xlabel('Smarts')
	plt.ylabel('Probability')
	plt.title('Histogram of IQ')

	line_up, = plt.plot([1, 2, 3], label='Line 2')
	line_down, = plt.plot([3, 2, 1], label='Line 1')
	plt.legend([line_up, line_down], ['Line Up', 'Line Down'])

	with plt.style.context(('mythesis')):
		plt.subplot(122)
	
		plt.xlabel('Smarts')
		plt.ylabel('Probability')
		plt.title('Histogram of IQ')
	
		line_up, = plt.plot([1, 2, 3], label='Line 2')
		line_down, = plt.plot([3, 2, 1], label='Line 1')
		plt.legend([line_up, line_down], ['Line Up', 'Line Down'])
	
		# Now add the legend with some customizations.
		legend = ax.legend(loc='upper center', shadow=True)

		# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
		frame = legend.get_frame()
		frame.set_facecolor('0.90')
		
		# Saving figure
		fig.savefig("foo.pdf", bbox_inches='tight')
		# To later use in latex do...
		fig.savefig("foo.pgf", bbox_inches='tight')
		#......on latex add/ $ usepackage{pgfplots}


	
	
