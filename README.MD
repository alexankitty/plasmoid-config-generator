# Plasmoid-Config-Generator
Generates a kcfg/xml file from a qml to make development of plasmoids faster.

## Usage
```sh
usage: Plasmoid Config Generator [-h] [-m MAINDIRECTORY] [-s] [-o OUTPUT] [-x EXTRAS] filename

Generates a kcfg/xml file for plasmoids to make development faster

positional arguments:
  filename              Filepath of your main config qml

options:
  -h, --help            show this help message and exit
  -m MAINDIRECTORY, --main-directory MAINDIRECTORY
                        Path to the main QML files
  -s, --single-file     Disables file recursion and assumes one file only
  -o OUTPUT, --output OUTPUT
                        Where to output the result
  -x EXTRAS, --extra-configs EXTRAS
                        Additional file to read for used configs that are not in the config interface

Written by Alexankitty 2023.
```

## Format
`property alias cfg_showToolTips: showToolTips.checked //type: bool label: Whether to show tooltips when hovering task buttons. default: true`
Make an inline comment for each cfg you want to include in your xml. Include the following: type:, label:, default:  
Optionally: include enum:, choices:  
choices: are expected to be space delimited.  
For blank strings, use either "" or ''.

### Extras
If you have configs that need saving that aren't exposed in the main config, make a separate file and pass it into the -x option.  
The only thing you need is the cfg_ name, and the comment.  
Example: `cfg_groupingLauncherUrlBlacklist //type: StringList label: The launcher URLs (usually .desktop file or executable URLs) of applications that should not have their tasks grouped. default: ''`