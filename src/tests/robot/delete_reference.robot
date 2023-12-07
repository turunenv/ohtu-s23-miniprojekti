*** Settings ***
Resource  resource.robot
Test Setup  Add References
Test Teardown  Empty Database


*** Test Cases ***
Delete Book Reference With Reference Key
    Input Delete Command
    Input Reference Key  test1
    Input  y
    List All References
    Output Should Not Contain  test1

Delete Article Reference With Reference Key
    Input Delete Command
    Input Reference Key  test2
    Input  y
    List All References
    Output Should Not Contain  AI In Customer Service

Delete Article With Reference Key Does Not Delete Book
    Input Delete Command
    Input Reference Key  test2
    Input  y
    List All References
    Output Should Contain  test1

*** Keywords ***
Add Book Reference
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    test1    tove jansson    muumit    1977    otava

Add Article Reference
    Input Add Command
    Input Reference Type  article
    Input Article Reference Fields    test2    Allix    AI In Customer Service    AI-Magazine    2023    11    50--51

List References
    Input List Command

Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application

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

Add References
    Add Book Reference
    Add Article Reference
