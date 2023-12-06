*** Settings ***
Resource  resource.robot
Test Setup  Run Application

*** Test Cases ***
Help Command Presents Available Commands And Their Short Describtions
    Input Help Command
#    Output Should Contain  Add a new reference by
#    Output Should Conatin  Return to the starting menu
#    Output Should Contain  Enter a file name to create a .bib file

App Prompts To Use Help Command
    Output Should Contain  Type "help" to list commands and their descriptions
