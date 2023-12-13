*** Settings ***
Resource  resource.robot
Test Setup  Empty Database
Test Teardown  Empty Database

*** Test Cases ***
Add Inproceedings Reference With Valid Fields And Unused Reference Key
    Input Add Command
    Input Reference Type    inproceedings
    Input Inproceedings Reference Fields    test1    Mary Jones    An Analysis of Robots    Proceedings of the Conference on Artificial Intelligence    2023
    List All References 
    Output Should Contain    Mary Jones


Add Inproceedings Reference With Invalid Year
    Input Add Command
    Input Reference Type    inproceedings
    Input Inproceedings Reference Fields With Invalid Year    test2    Pandora Rosier    Ethics In Computer Science    Proceedings of the International Conference    1980s    1982
    List All References 
    Output Should Contain    Pandora Rosier
    Output Should Contain    1982

*** Keywords ***
Input Inproceedings Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${booktitle}  ${year}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${booktitle}
    Input  ${year}
    Run Application

Input Inproceedings Reference Fields With Invalid Year
    [Arguments]  ${ref_key}  ${author}  ${title}  ${booktitle}  ${invalid_year}  ${year}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${booktitle}
    Input  ${invalid_year}
    Input  ${year}
    Run Application

Empty Database
    Clear Database
