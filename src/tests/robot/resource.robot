*** Settings ***
Library  ../../AppLibrary.py

*** Keywords ***
Input Help Command
    Input  help

Input Add Command
    Input  add

Input List Command
    Input  list

Input Delete Command
    Input  delete

Input File Command
    Input  file

Input Doi Command
    Input  doi

Input Tag Command
    Input  tag

Input Search Command
    Input  search

Input Reference Type
    [Arguments]  ${ref_type}
    Input  ${ref_type}

Input Reference Key
    [Arguments]  ${ref_key}
    Input  ${ref_key}

Input File Name
    [Arguments]  ${file_name}
    Input  ${file_name}
