#!/usr/bin/python
import os,subprocess

def writeTex( file , string ):
  file.write(string+'\n')

def addBlockA( outFile , infoString ):
  if infoString == '':
    writeTex(outFile,'\\blockA{}')
  else:
    writeTex(outFile,'\\blockA{{{0}}}'.format(infoString))

def AddSenator( senatorName , officeAddress ):
  AddRep(senatorName,officeAddress,isSenator=True)

def AddRep( repName , officeAddress , memberGender = '', isSenator = False ):

  repNameComponents = repName.split(' ')
  repFirstName = repNameComponents[0]
  repSurname = ' '.join(repNameComponents[1:])

  officeAddressComponents = officeAddress.split(' ')
  officeNumber = officeAddressComponents[0]
  officeBuildingName = officeAddressComponents[1]
  officeBuildingClass = ' Senate ' if isSenator else ' House '
  officeBuilding = officeBuildingName + officeBuildingClass + 'Office Building'

  if isSenator:               memberTitle = 'Senator'
  elif memberGender == 'M':   memberTitle = 'Congressman'
  elif memberGender == 'F':   memberTitle = 'Congresswoman'
  elif memberGender == 'GN':  memberTitle = 'Congressperson'
  else: print("You have not provided a valid memberGender for representative {0}".format(repName))

  REPS[repSurname] = [repFirstName,officeNumber,officeBuilding,memberTitle]

## Functions defined above

REPS = {}
AddSenator('Tom Carper','513 Hart')
AddRep('Mike Levin','1030 Longworth', 'M')
AddRep('Sara Jacobs','1232 Longworth', 'F')



LETTERSROOT = 'Meeting_Request_Letters'

if not os.path.isdir(LETTERSROOT):
  print("Making output directory {0}".format(LETTERSROOT))
  os.makedirs(LETTERSROOT,exist_ok=True)

for rep,repData in REPS.items():

  print('Generating .tex for {0} {1}...'.format(repData[3],rep))

  outDir = os.path.join(LETTERSROOT,rep)
  if not os.path.isdir(outDir):
    print("Making output directory {0}".format(outDir))
    os.makedirs(outDir,exist_ok=True)
  surnameCompressed = ''.join(rep.split(' '))
  outFileName = '{0}_HEP_Meeting_Request_Letter_March2021.tex'.format(surnameCompressed)
  outFile = open(os.path.join(outDir,outFileName),'w')

  writeTex(outFile,'\input{../../Header.tex}')
  writeTex(outFile,'\\begin{document}')

  writeTex(outFile,'%----------------------------------------------------------------------------------------')
  writeTex(outFile,'%	TO ADDRESS')
  writeTex(outFile,'%----------------------------------------------------------------------------------------')
  writeTex(outFile,'\\begin{letter}{')
  writeTex(outFile,'')
  writeTex(outFile,'The Honorable {0} {1}\\\\'.format(repData[0],rep))
  chamber = 'Senate' if repData[3] == 'Senator' else 'House of Representatives'
  writeTex(outFile,'United States {0}\\\\'.format(chamber))
  writeTex(outFile,'{0} {1}\\\\'.format(repData[1],repData[2]))
  writeTex(outFile,'Washington, D.C. 20510' if repData[3] == 'Senator' else 'Washington, D.C. 20515')
  writeTex(outFile,'')
  writeTex(outFile,'}')

  writeTex(outFile,'%----------------------------------------------------------------------------------------')
  writeTex(outFile,'%	LETTER CONTENT')
  writeTex(outFile,'%----------------------------------------------------------------------------------------')

  writeTex(outFile,'\\opening{Dear ' + '{0} {1}'.format(repData[3],rep) + ':}')
  writeTex(outFile,'')

  # This is where you add a half sentence explaining your connection to this district. This string will be appended to an existing sentence, so don't capitalize the first word unless it needs to be capitalized!
  if rep == 'Carper':
      connectionString = "We previously met when you visited the MIT chapter of the Phi Sigma Kappa fraternity, where your son and my friend, Chris Carper, and I lived and when I met with your office on a prior trip on March 29, 2017."
  elif rep == 'Jacobs':
      connectionString = "I currently live in the University Heights neighborhood of San Diego in your district."
  elif rep == 'Levin':
      connectionString = "I was previously contacted by Fracine Busby, District Director in your office, congratulating my colleagues and I on receiving a \$5,000,000 National Science Foundation grant for our research at the San Diego Supercomputer Center entitled \emph{Exploring Neural Network Processors for AI in Science and Engineering}."
  else:
      connectionString = ""

  addBlockA(outFile,connectionString)
  writeTex(outFile,'')
  writeTex(outFile,'\\blockB{}')
  writeTex(outFile,'')
  writeTex(outFile,'\signoff')
  writeTex(outFile,'')
  writeTex(outFile,'\end{letter}')
  writeTex(outFile,'\end{document}')

  outFile.close()

  # Go to the directory created for this rep and compile the .tex
  owd = os.getcwd()
  os.chdir(outDir)
  #os.system('pwd')
  # Compile the .tex
  p = subprocess.Popen(['pdflatex', '-interaction', 'nonstopmode', outFileName])
  p.communicate()
  #os.system('pdflatex {0}'.format(outFileName))
  # Go back to the scripts directory
  os.chdir(owd)
