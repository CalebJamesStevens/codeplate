import re
#import
import json
import os
import re
import sys

# Gets current directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Loads config file
with open(os.path.join(__location__, f'codeplateconfig.json'), 'r') as configFile:
  config=configFile.read()
config=json.loads(config)

# Get file data
def getFileData(fileName, fileType):
  configDefault = ''
  codeplateDir = ''
  if fileType == "plan":
    configDefault = 'plans'
    codeplateDir = 'Plans'
  elif fileType == "platter":
    configDefault = 'platters'
    codeplateDir = 'Platters'
  elif fileType == "tpl":
    configDefault = 'templates'
    codeplateDir = 'Templates'

  if re.search('\.', fileName):
    with open(os.path.join(__location__, f'Codeplate/{codeplateDir}/{fileName}'), 'r') as _file:
        fileData=_file.read()
    return {"fileData": fileData, "fileName": fileName}
  else:
    nameOfRef = config['defaults'][configDefault][fileName]
    with open(os.path.join(__location__, f'Codeplate/{codeplateDir}/{nameOfRef}'), 'r') as _file:
        fileData=_file.read()
    return {"fileData": fileData, "fileName": nameOfRef}

# Code for replacing variable names in a platter
def replacePlatterVars(data, variables, answers):
  keys = data.copy().keys()
  for key in keys:
    if isinstance(data[key], list):
      objKeys = data[key][2].copy().keys()
      for oKey in objKeys:
        if data[key][2][oKey] in variables:
          if data[key][2][oKey] not in answers.keys():
            answers[data[key][2][oKey]] = input(f'Variable {data[key][2][oKey]} not supplied for {oKey}.\nWhat will be it\'s value?\n')
          data[key][2][oKey] = answers[data[key][2][oKey]]
    if key in variables:
      if key not in answers.keys():
        answers[key] = input(f'Variable {key} not supplied for {key}.\nWhat will be it\'s value?\n')
      data[answers[key]] = data.pop(key)
      if isinstance(data[answers[key]], dict):
        replacePlatterVars(data[answers[key]], variables, answers)
    elif isinstance(data[key], dict):
      replacePlatterVars(data[key], variables, answers)

# Code for parsing json object and adding correct files/dirs with correct configs
def createPlan(data, parent =__location__):
  for key in data.keys():
    if isinstance(data[key], dict):
      os.mkdir(os.path.join(parent, key))
      createPlan(data[key], os.path.join(parent, key))
    if isinstance(data[key], str):
      createTemplate(data[key], key, {}, parent)
    if isinstance(data[key], list):
      if "platter" in data[key][1] and data[key][1]["platter"] == True:
        createPlatter(parent, data[key][0], data[key][2])
      else:
        createTemplate(data[key][0], key, data[key][2], parent)

def createPlatter(parent =__location__, platterRef ="", answers ={}):
  platterData = getFileData(platterRef, 'platter')["fileData"]
  platterData = json.loads(platterData)
  replacePlatterVars(platterData["platter"], platterData["config"], answers)
  createPlan(platterData["platter"], parent)

def raplaceTemplateVariables(data, answers, fileName):
  replacedData = data
  attributesArray = re.findall("codeplate_[A-z]*[0-9]*[_]*", replacedData)
  dedupedAttributes = {}
  for attribute in attributesArray:
    dedupedAttributes[attribute] = True

  for attribute in dedupedAttributes.keys():
    if attribute not in answers:
      answers[attribute] = input(f'Variable {attribute} not supplied for {fileName}.\nWhat will be it\'s value?\n')

  for attribute in dedupedAttributes:
    replacedData = re.sub(attribute, answers[attribute], replacedData)

  return replacedData

def createTemplate(templateName ='', newFileName ='', answers ={}, parent=__location__):
  data = getFileData(templateName, 'tpl')

  extension = "."+re.sub(".*?[\.]", '', newFileName, 1)
  givenBaseName = re.sub('\..*', '', newFileName)
  templateExtenstion = "."+re.sub(".*?[\.]", '', data["fileName"], 1)


  name = ''
  if f'{givenBaseName}{extension}' == f'{givenBaseName}{templateExtenstion}':
      name = newFileName
  else:
      name = f'{newFileName}{templateExtenstion}'

  dataToWrite = raplaceTemplateVariables(data["fileData"], answers, name)

  fileToWrite = open(os.path.join(parent, name), "a")

  fileToWrite.write(dataToWrite)
  fileToWrite.close()


# Plan name passed into cli
if sys.argv[1] == "plan":
  fileData = getFileData(sys.argv[2], 'plan')["fileData"]
  createPlan(json.loads(fileData))
elif sys.argv[1] == "platter":
  try:
    answers = json.loads(sys.argv[3])
    createPlatter(__location__, sys.argv[2], answers)
  except IndexError:
    createPlatter(__location__, sys.argv[2])
elif sys.argv[1] == "tpl":
  filename = ''
  directory = ''
  answers = {}

  for i in sys.argv:
    if re.search("answers=", i):
      answers = json.loads(re.sub("answers=", '', i))
    if re.search("filename=", i):
      filename = re.sub("filename=", '', i)
    if re.search("directory=", i):
      directory = re.sub("directory=", '', i)

  if filename == '':
    filename = input("Filename:\n")

  # if not directory == '':
  #   if re.search("\/", directory):
  #
  #   else:
  #     directory = config["directories"][directory]

  createTemplate(sys.argv[2], filename, answers, parent=os.path.join(__location__, directory))
else:
  print('Please provide a type. Ex: python3 Codeplate.py tpl BasicComponent.js')
