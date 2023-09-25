import argparse
import sys
import re
import os
import types

xmlHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<kcfg xmlns="http://www.kde.org/standards/kcfg/1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.kde.org/standards/kcfg/1.0
      http://www.kde.org/standards/kcfg/1.0/kcfg.xsd" >
  <kcfgfile name=""/>

  <group name="General">'''

xmlFooter = '''
  </group>

</kcfg>
'''

class Config(object):
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

parser = argparse.ArgumentParser(
    prog='Plasmoid Config Generator',
    description='Generates a kcfg/xml file for plasmoids to make development faster',
    epilog='Written by Alexankitty 2023.',
    add_help=True)

parser.add_argument('filename', help='Filepath of your main config qml')
parser.add_argument('-m', '--main-directory', help='Path to the main QML files', dest='mainDirectory')
parser.add_argument('-s', '--single-file',action='store_true', help='Disables file recursion and assumes one file only', dest='singleFile')
parser.add_argument('-o', '--output', help='Where to output the result', dest='output')
parser.add_argument('-x', '--extra-configs', help='Additional file to read for used configs that are not in the config interface', dest='extras')

args = parser.parse_args()

filename = args.filename
singleFile = args.singleFile
output = args.output
mainDirectory = args.mainDirectory
extras = args.extras

files = [None] * 0
if not singleFile:
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        if('source' in line):
            files.append(re.findall(r'"(.*?)"', line)[0])
    f.close()
else:
    files.append(filename)

if extras:
    files.append(extras)

if mainDirectory:
    workingDir = os.path.abspath(mainDirectory)
else:
    workingDir = os.path.dirname(os.path.abspath(filename))

if output:
    outputPath = os.path.abspath(output)
else:
    outputPath = os.getcwd() + "/main.xml"

configEntries = [None] * 0
for file in files:
    path = workingDir + "/" + file
    with open(path, "r") as f:
        lines = f.readlines()
    for line in lines:
        if("cfg_" in line):
            config = re.findall(r'(?<=\/\/).*', line)
            if config:
                config = config[0] #Extract the entry.
            else:
                print(f"Warning: no comment entry for:\n{line}")
                continue
            print(config)
            if config:
                names = re.findall(r'(\w+?)(?=:)', config)
                values = re.findall(r'([^ :][^:]*)(?!\w*?:)', config)
                configEntry = Config()
                for name, value in zip(names, values):
                    if "''" in value:
                        value = ''
                    if '""' in value:
                        value = ""
                    configEntry[name] = value
                configEntry["name"] = re.findall(r'(?<=cfg_)\w+?(?=:)', line)[0]
                configEntries.append(configEntry)

print(files)
print(workingDir)
print(outputPath)
for config in configEntries:
    xml = xmlHeader
    if config.type == "enum":
        choices = config.choices.split()
        choiceXml = ''
        for choice in choices:
            choiceXml += f'''
            <choice name="{choice}"/>
            '''
        xml += f'''
    <entry name="{config.name}" type="{config.type}">
      <label>{config.label}</label>
      <choices>
{choiceXml}
      </choices>
      <default>{config.default}</default>
    </entry>'''
    else:
        xml += f'''
    <entry name="{config.name}" type="{config.type}">
      <label>{config.label}</label>
      <default>{config.default}</default>
    </entry>'''
    xml += xmlFooter

print(xml)