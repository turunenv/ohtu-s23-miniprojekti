*** Settings ***
Resource  resource.robot
Test Setup  Empty Database And Add Prior Article
Test Teardown  Empty Database

*** Test Cases ***
Add Doi Reference Using Valid Doi and Unused Reference Key
    Input Doi Command
    Input Doi Reference Fields  test12  10.25008/abdiformatika.v1i2.144  y
    List All References
    Output Should Contain  test12

Add Doi Reference Using Valid Fields but Unsupported Reference Type
    Input Doi Command
    Input Doi Reference Fields  test13  10.5040/9781838712181.0004  y
    Output Should Contain  This reference type is not supported

Add Doi Reference Using Valid Fields but Information Missing
    Input Doi Command
    Input Doi Reference Fields  test14  10.5152/iao.2023.22771  y
    Output Should Contain  Some necessary information was missing

Add Doi Reference Using Valid Doi and Invalid Reference Key
    Input Doi Command
    Input Doi Reference Fields Invalid Key  test11  test15  10.25008/abdiformatika.v1i2.144  y
    List All References
    Output Should Contain  test15

Add Doi Reference Using Invalid Doi and Unused Reference Key
    Input Doi Command
    Input Doi Reference Fields  test16  10.25008/abdiformatika.v1i2.144WRONG_URL  y
    Output Should Contain  DOI not found

*** Keywords ***
Input Doi Reference Fields
    [Arguments]  ${ref_key}  ${doi}  ${confirmation}
    Input  ${ref_key}
    Input  ${doi}
    Input  ${confirmation}
    Run Application

Input Doi Reference Fields Invalid Key
    [Arguments]  ${ref_key1}  ${ref_key2}  ${doi}  ${confirmation}
    Input  ${ref_key1}
    Input  ${ref_key2}
    Input  ${doi}
    Input  ${confirmation}
    Run Application

Empty Database
    Clear Database

Empty Database And Add Prior Article
    Empty Database
    Add Prior Article

Add Prior Article
    Input Doi Command
    Input Doi Reference Fields  test11  10.1093/ajae/aaq063  y
