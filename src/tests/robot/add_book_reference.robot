*** Settings ***
Resource  resource.robot
Test Setup  Empty Database
Test Teardown  Empty Database

*** Test Cases ***
Add Book Reference With Valid Fields And Unused Reference Key
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    test1    tove jansson    muumit    1977    otava
    List All References 
    Output Should Contain    test1

Add Book Reference With Invalid Year
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields With Invalid Year    test2    tove jansson    muumit    1970's  1977    otava
    List All References 
    Output Should Contain    test2

*** Keywords ***
Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application

Input Book Reference Fields With Invalid Year
    [Arguments]  ${ref_key}  ${author}  ${title}  ${invalid_year}  ${valid_year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${invalid_year}
    Input  ${valid_year}
    Input  ${publisher}
    Run Application

Empty Database
    Clear Database
