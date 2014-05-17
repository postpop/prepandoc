import string
import sys
import os
import subprocess

print('PANDOC preprocessor')

# check input arguments
if len(sys.argv)==1:
	sys.exit('   need to provide a file name as an argument.')

# check whether pandoc command is available
command = ['pandoc']
try:
	subprocess.call([command[0], '--version'],stdout=subprocess.PIPE)
except:
	sys.exit('   Cannot find pandoc command - add bin to path!')


# try to open the file
fileName = sys.argv[1]
try:
	f = open(fileName, 'r')
except:
	sys.exit('   error opening ' + fileName)

# parse file and build argument-value list
t = f.read()
tt = string.split(t,os.linesep)
# identify instruction lines starting with metaID=!!!
print('   parsing ' + fileName + ' for instructions.')
metaID = "!!!"
for line in tt:
	if line.startswith(metaID):
		partLine = line[4:].partition(' ')
		print(partLine)
		if len(partLine[0])==1:# single character arguments -aval
			arg = '-' + partLine[0] + partLine[2]
		elif len(partLine[2])==0:
			arg = '--' + partLine[0] 
		else:# multi-character arguments --arg=val
			arg = '--' + partLine[0] + '=' + partLine[2]
		command.append(arg)
print('   ' + str(len(command)-1) + ' instructions found.')
command.append(fileName)
print('   calling command:')
print('   ' + ' '.join(command))
out = subprocess.call(command)
print('DONE.')