*** Settings ***
Resource  resource.robot
Test Setup  One Reference
Test Teardown  Empty Database

*** Test Cases ***
Search With Valid Tag
    Input Search Command
    Input Search Tag  YA
    Run Application

    Output Should Contain  Hunger Games

Search With Invalid Tag
    Input Search Command
    Input Search Tag  Non-existing tag
    Run Application

    Output Should Contain  Not an existing tag

*** Keywords ***
One Reference
    Clear Database
    Add Book Reference
    Add Tag

Add Book Reference
    Input Add Command
    Input Reference Type    book
    Input Book Reference Fields    test1    Suzanne Collins    Hunger Games    2008    Scholastic

Input Book Reference Fields
    [Arguments]  ${ref_key}  ${author}  ${title}  ${year}  ${publisher}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${year}
    Input  ${publisher}
    Run Application

Input Tag Fields
    [Arguments]  ${tag}  ${ref_key}
    Input  ${tag}
    Input  ${ref_key}

Add Tag
    Input Tag Command
    Input Tag Fields  YA  test1
    Run Application

Input Search Tag
    [Arguments]  ${tag}
    Input  ${tag}


Empty Database
    Clear Database
