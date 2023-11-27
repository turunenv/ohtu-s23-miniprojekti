*** Settings ***
Resource  resource.robot
Test Setup  Clear Database

*** Test Cases ***
Add Book Reference With Valid Fields And Unused Reference Key
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    abc1    tove jansson    muumit    1977    otava
    List All References 
    Output Should Contain    muumit

*** Keywords ***
Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application




