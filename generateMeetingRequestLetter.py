#!/usr/bin/python
import os,subprocess

def writeTex( file , string ):
  file.write(string+'\n')

def addBlockA( outFile , infoString ):
  if infoString == '':
    writeTex(outFile,'\\blockA{}')
  else:
    writeTex(outFile,'\\blockA{, and ' + '{0}'.format(infoString) + '}')

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
  else: print "You have not provided a valid memberGender for representative {0}".format(repName)
  
  REPS[repSurname] = [repFirstName,officeNumber,officeBuilding,memberTitle]

## Functions defined above

REPS = {}

AddRep('Alma Adams','2436 Rayburn','F')
AddRep('Mark Amodei','104 Cannon','M')
AddRep('Ted Budd','118 Cannon','M')
AddRep('Joe Cunningham','423 Cannon','M')
AddRep('Tom Emmer','315 Cannon','M')
AddRep('Bob Gibbs','2446 Rayburn','M')
AddRep('Richard Hudson','2112 Rayburn','M')
AddRep('Dave Joyce','1124 Longworth','M')
AddRep('Raja Krishnamoorthi','115 Cannon','M')
AddRep('Nita Lowey','2365 Rayburn','F')
AddRep('Sean Patrick Maloney','2331 Rayburn','M')
AddRep('David McKinley','2239 Rayburn','M')
AddRep('Carol Miller','1605 Longworth','F')
AddRep('Joe Morelle','1317 Longworth','M')
AddRep('Jamie Raskin','412 Cannon','M')
AddRep('Tim Ryan','1126 Longworth','M')
AddRep('Bonnie Watson Coleman','2442 Rayburn','F')

AddSenator('Shelly Moore Capito','172 Russell')
AddSenator('Tim Scott','104 Hart')

WORKING_DIR = '/Users/hyperfiner/Documents/Academic/Fermilab/HEP_Advocacy/DC_Trip_2019'
SCRIPTSROOT = '{0}/2019-HEP-MeetingRequest-scripts'.format(WORKING_DIR)
LETTERSROOT = '{0}/Meeting_Request_Letters'.format(WORKING_DIR)

if not os.path.isdir(LETTERSROOT):
  print "Making output directory {0}".format(LETTERSROOT)
  os.system( "mkdir {0}/{1}".format(WORKING_DIR,LETTERSROOT) )

for rep,repData in REPS.items():

  print 'Generating .tex for {0} {1}...'.format(repData[3],rep)

  outDir = '{0}/{1}'.format(LETTERSROOT,rep)
  if not os.path.isdir(outDir): 
    print "Making output directory {0}".format(outDir)
    os.system( "mkdir '{0}'".format(outDir) )
  surnameCompressed = ''.join(rep.split(' '))
  outFileName = '{0}_HEP_Meeting_Request_Letter_March2019.tex'.format(surnameCompressed)
  outFile = open('{0}/{1}'.format(outDir,outFileName),'w')
 
  writeTex(outFile,'\input{../../2019-HEP-MeetingRequest-scripts/Header.tex}')
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
  writeTex(outFile,'Washington, D.C. 20515')
  writeTex(outFile,'')
  writeTex(outFile,'}')

  writeTex(outFile,'%----------------------------------------------------------------------------------------')
  writeTex(outFile,'%	LETTER CONTENT')
  writeTex(outFile,'%----------------------------------------------------------------------------------------')

  writeTex(outFile,'\\opening{Dear ' + '{0} {1}'.format(repData[3],rep) + ':}')
  writeTex(outFile,'')

  # This is where you add a half sentence explaining your connection to this district. This string will be appended to an existing sentence, so don't capitalize the first word unless it needs to be capitalized!
  if rep == 'Gibbs':              connectionString = "I received my Bachelor's degree in physics at Kenyon College, in your district"
  elif rep == 'Lowey':            connectionString = "I grew up in Westchester County, where my parents still live and are registered voters"
  elif rep == 'Patrick Maloney':  connectionString = "I am a native New Yorker, having grown up in Westchester county. I have family and friends throughout the State, including in your district"
  elif rep == 'Cunningham':       connectionString = "my parents have recently settled in your district to begin their retirement"
  elif rep == 'Scott':            connectionString = "my parents have recently settled in South Carolina to begin their retirement"
  elif rep == 'Watson Coleman':   connectionString = "I have close family that are long-time residents of, and registered voters in, your district"
  else:                           connectionString = ""

  addBlockA(outFile,connectionString)
  writeTex(outFile,'')
  writeTex(outFile,'\\blockB{}')
  writeTex(outFile,'')
  writeTex(outFile,'\signoff{210}')
  writeTex(outFile,'')
  writeTex(outFile,'\end{letter}')
  writeTex(outFile,'\end{document}')

  outFile.close()

  # Go to the directory created for this rep and compile the .tex
  os.chdir(outDir)
  #os.system('pwd')
  # Compile the .tex
  p = subprocess.Popen(['pdflatex', '-interaction', 'nonstopmode', '{0}/{1}'.format(outDir,outFileName)])
  p.communicate()
  #os.system('pdflatex {0}'.format(outFileName))
  # Go back to the scripts directory 
  os.chdir(SCRIPTSROOT)
