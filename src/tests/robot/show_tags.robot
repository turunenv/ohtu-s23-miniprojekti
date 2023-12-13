*** Settings ***
Resource  resource.robot
Test Setup  Add Tags And References
Test Teardown  Empty Database

*** Test Cases ***
Tags Shows All Existing Tags
    Input Tags Command
    Run Application

    Output Should Contain  YA
    Output Should Contain  All

Tags Shows Amount Of References With Each Tag
    Input Tags Command
    Run Application

    Output Should Contain  2

*** Keywords ***
Add Tags And References
    Clear Database
    Add Book Reference
    Add Inproceedings Reference
    Add Tag One
    Add Tag Two
    Add Tag Three

Add Book Reference
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    test1    Suzanne Collins    Hunger Games    2008    Scholastic

Add Inproceedings Reference
    Input Add Command
    Input Reference Type  inproceedings
    Input Inproceedings Reference Fields    test4    Mary Jones    An Analysis of Robots    Proceedings of the Conference on Artificial Intelligence    2023

Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application

Input Inproceedings Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${booktitle}  ${year}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${booktitle}
    Input  ${year}
    Run Application

Input Tag Fields
    [Arguments]  ${tag}  ${ref_key}
    Input  ${tag}
    Input  ${ref_key}

Add Tag One
    Input Tag Command
    Input Tag Fields  YA  test1
    Run Application

Add Tag Two
    Input Tag Command
    Input Tag Fields  All  test4
    Run Application

Add Tag Three
    Input Tag Command
    Input Tag Fields  All  test1
    Run Application


Empty Database
    Clear Database
