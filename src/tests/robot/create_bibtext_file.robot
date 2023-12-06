*** Settings ***
Resource  resource.robot
Library  OperatingSystem
Test Setup  One Reference
Test Teardown  Empty Database


*** Test Cases ***
Create Bibtext File
    Input File Command
    Input File Name  testfile
    Run Application
    
    Output Should Contain  1 references succesfully written to testfile
    File Should Exist  ./testfile.bib
    
    Delete Test File  ./testfile.bib


*** Keywords ***
One Reference
    Clear Database
    Add Book Reference

Add Book Reference
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    test1    tove jansson    muumit    1977    otava

Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application

Empty Database
    Clear Database
