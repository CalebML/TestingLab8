from unittest import TestCase
#import os
import glob
import inspect
import Source
#from __init__ import __all__
import importlib

error = None
moduleStrings = []
modules = []
#parameters for functions   (optional for all)
known_parameters = {'index': 10}      
#Parameters for classes     (required only if the class takes more than 1 parameter)
classDict = {'pyTona.question_answer.QA':{'question':'Test Question', 'answer':'Test Answer'},
             'Source.pyTona.question_answer.QA':{'question':'Test Question', 'answer':'Test Answer'}}
#internalClassDict = {}

class SanityTeat(TestCase):
    
    def setUp(self):
        global error
        error = None
        global moduleStrings
        global classDict
        try:
            # add all modules in the source folder to "modules" list
            moduleStrings = glob.glob("Source"+"/*/*.py")
            moduleStrings = moduleStrings + glob.glob("Source"+"/*.py")
            print moduleStrings    #On test failure this will display all found modules
        except:
            error = error + "Error finding module strings" + '\n'
            #print error
        
        print " "
        #test = [ os.path.basename(f)[:-3] for f in modules]
        #print test

        global modules
        modules = []
        
        length = len(moduleStrings)
        i = 0
        try:
            while(length > i):
                #edit the strings
                print " "
                print moduleStrings[i]    
                moduleStrings[i] = moduleStrings[i].split('.')[0]
                moduleStrings[i] = moduleStrings[i].replace('\\', '.')
                #print for test output
                print moduleStrings[i]

                modules.append( importlib.import_module(moduleStrings[i]) )
                print modules[i]
                i += 1
        except:
            error = error + "Error converting strings to modules" + '\n'
            #print error        

        
    def test_sanity(self):
        global error
        global moduleStrings
        global known_parameters
        global classDict
        global modules
        
        if(not error):
            print " "
            length = len(modules)
            i = 0       #module count
            j = 0       #member count
            classes = []
            funcs = []
            print str(length) + " modules"

            #get members (classes and functions) from found modules
            try:
                while (length > i):
                    members = dir(modules[i])
                    print " "
                    print moduleStrings[i]
                    #print members

                    j = 0
                    numMembers = len(members)

                    while(numMembers > j):
                        test = moduleStrings[i] + '.' + members[j]
                        testFunc = getattr(modules[i], members[j])
                        #print test
                        
                        #print inspect.isclass( testFunc )
                        if( inspect.isclass( testFunc ) ):
                            print test + " is a class"
                            classes.append(testFunc)

                        elif( inspect.isfunction( testFunc ) ):
                            print test + " is a callable function"
                            funcs.append(testFunc)
                        
                        j += 1
                    i += 1
            except:
                error = error + "Error getting members from modules" + '\n'

            #Instaniate all classes
            length = len(classes)
            i = 0
            
            print " "
            print "Testing classes:"
            try:
                while(length > i):
                    print classes[i]
                    parameters = {}
                    testName = classes[i].__module__ + '.' + classes[i].__name__

                    if( (testName in classDict) ):
                        parameters = classDict[testName]
                        print "using parameters: " + str(parameters)
                        
                    classes[i](**parameters)
                    print "Success"
                    i += 1
            except:
                error = error + "failed to instaniate class " + str (classes[i]) + '\n'

            length = len(funcs)
            i = 0
            
            print " "
            print "Testing functions:"
            try:
                while(length > i):
                    print funcs[i]
                    
                    args = inspect.getargspec(funcs[i])
                    numArgs = len(args[0])
                    #print numArgs

                    j = 0
                    parameters = {}
                    while(numArgs > j):
                        if( args[0][j] in known_parameters ):
                            print "using known parameter(s): " + str(known_parameters[args[0][j]])
                            parameters[args[0][j]] = known_parameters[args[0][j]]
                        else:
                            parameters[args[0][j]] = 50
                        j +=1
                    #print parameters
                    funcs[i](**parameters)
                    print "Success"
                    #print " "
                    i += 1
            except:
                error = error + "failed to run function " + str(funcs[i]) + '\n'
            

        if (error):
            print " "
            print "Error: " + error
        self.assertTrue(error == None)


