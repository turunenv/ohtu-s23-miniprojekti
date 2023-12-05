*** Settings ***
Resource  resource.robot
Test Setup  Empty Database
Test Teardown  Empty Database

*** Test Cases ***
Add Article Reference With Valid Fields And Unused Reference Key
    Input Add Command
    Input Reference Type    article
    Input Article Reference Fields    test2    Allix    AI In Customer Service    AI-Magazine    2023    11    50-51
    List All References
    Output Should Contain    AI-Magazine

*** Keywords ***
Input Article Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${journal}  ${year}  ${volume}  ${pages}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${journal}
    Input  ${year}
    Input  ${volume}
    Input  ${pages}
    Run Application

Empty Database
    Clear Database
