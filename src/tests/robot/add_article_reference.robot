*** Settings ***
Resource  resource.robot
Test Setup  Empty Database And Add Prior Article
Test Teardown  Empty Database

*** Test Cases ***
Add Article Reference With Valid Fields And Unused Reference Key
    Input Add Command
    Input Reference Type    article
    Input Article Reference Fields    test2    Allix    AI In Customer Service    AI-Magazine    2023    11    50--51
    List All References
    Output Should Contain    AI-Magazine

Add Article Reference With Invalid Reference Key
    Input Add Command
    Input Reference Type  article
    Input Article Reference Fields With Invalid Reference Key  test3  test4  Allix  AI In Customer Service  AI-Magazine  2023  11    50--51
    List All References
    Output Should Contain  test4

Add Article Reference With Invalid Year
    Input Add Command
    Input Reference Type    article
    Input Article Reference Fields With Invalid Value   test5    Allix    AI In Customer Service    AI-Magazine    1970's  2023    11    50--51
    List All References
    Output Should Contain    test5

Add Article Reference With Invalid Volume
    Input Add Command
    Input Reference Type    article
    Input Article Reference Fields With Invalid Value   test6    Allix    AI In Customer Service    AI-Magazine    2023    v11  11   50--51
    List All References
    Output Should Contain    test6

Add Article Reference With Invalid Pages
    Input Add Command
    Input Reference Type    article
    Input Article Reference Fields With Invalid Value   test7    Allix    AI In Customer Service    AI-Magazine    2023    11    50-51  50--51
    List All References
    Output Should Contain    test7

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

 Input Article Reference Fields With Invalid Reference Key
    [Arguments]  ${ref_key}  ${second_key}  ${author}  ${title}  ${journal}  ${year}  ${volume}  ${pages}
    Input  ${ref_key}
    Input  ${second_key}
    Input  ${author}
    Input  ${title}
    Input  ${journal}
    Input  ${year}
    Input  ${volume}
    Input  ${pages}
    Run Application

Input Article Reference Fields With Invalid Value
    [Arguments]  ${ref_key}  ${author}  ${title}  ${journal}  ${maybeValid1}  ${maybeValid2}  ${maybeValid3}  ${maybeValid4}
    Input  ${ref_key}
    Input  ${author}
    Input  ${title}
    Input  ${journal}
    Input  ${maybeValid1}
    Input  ${maybeValid2}
    Input  ${maybeValid3}
    Input  ${maybeValid4}
    Run Application

Empty Database
    Clear Database

Empty Database And Add Prior Article
    Empty Database
    Add Prior Article

Add Prior Article
    Input Add Command
    Input Reference Type  article
    Input Article Reference Fields  test3  Connor  How to Guide for Something  Cyber Life  2016  3  9--13
