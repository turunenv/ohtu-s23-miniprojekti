*** Settings ***
Resource  resource.robot
Test Setup  Add Book Reference
Test Teardown  Empty Database


*** Test Cases ***
Delete Book Reference With Reference Key
    Input Delete Command
    Input Reference Key  test1
    Input  y
    Output Should Not Contain  test1

*** Keywords ***
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
