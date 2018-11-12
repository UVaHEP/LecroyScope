import os

rawNames= os.listdir ('/eos/user/t/tanderso/2018-11-CMSTiming/Raw/') # get all files' and folders' names in the current directory
rawDirs = []
for name in rawNames: # loop through all the files and folders
    if not os.path.isdir(os.path.join(os.path.abspath("."), name)): # check whether the current object is a folder 
        rawDirs.append(name)
#print rawDirs

rootNames= os.listdir ('/eos/user/t/tanderso/2018-11-CMSTiming/Root/') # get all files' and folders' names in the current directory
rootDirs = []
for name in rootNames: # loop through all the files and folders
    if not os.path.isdir(os.path.join(os.path.abspath("."), name)): # check whether the current object is a folder 
        rootDirs.append(name.rstrip('.root'))
#print rootDirs

nProcessed = 0

for rawRun in rawDirs:
    if rawRun not in rootDirs:
        outfile = rawRun.replace('Raw', 'Root')
        outfile = '/eos/user/t/tanderso/2018-11-CMSTiming/Root/' + outfile + '.root'
        os.system('python LecroyBinProcessor2.py -d /eos/user/t/tanderso/2018-11-CMSTiming/Raw/{0} -o {1}'.format(rawRun, outfile))        
        #print ('python LecroyBinProcessor2.py -d /eos/user/t/tanderso/2018-11-CMSTiming/Raw/{0} -o {1}'.format(rawRun, outfile))        
        nProcessed = nProcessed + 1
    else:
        print "Run {0} already processed... SKIPPING...".format(rawRun)

print "======================================="
print " -----  Processed {0} new runs  ----- ".format(nProcessed)
print "======================================="
