*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${NAME}    Test User
${EMAIL}   testuser@example.com
${PASSWORD}    TestPassword123
${FIRST_NAME}   Test
${LAST_NAME}    User
${COMPANY}      Test Company
${ADDRESS1}     123 Test St
${ADDRESS2}     Apt 4
${COUNTRY}      United States
${STATE}        Test State
${CITY}         Test City
${ZIPCODE}      12345
${MOBILE}       1234567890

*** Test Cases ***
Register User
    [Documentation]    Test case to register a new user
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Click Link    Signup / Login
    Element Should Be Visible    //h2[contains(text(), 'New User Signup!')]
    Input Text    //*[@id='form']/input[@placeholder='Name']    ${NAME}
    Input Text    //*[@id='form']/input[@placeholder='Email']    ${EMAIL}
    Click Button    //*[@id='form']/button[contains(text(), 'Signup')]
    Element Should Be Visible    //h2[contains(text(), 'ENTER ACCOUNT INFORMATION')]
    Select Radio Button    //*[@id='id_gender']    Mr.
    Input Text    //*[@id='name']    ${NAME}
    Input Text    //*[@id='email']    ${EMAIL}
    Input Text    //*[@id='password']    ${PASSWORD}
    Select From List By Index    //*[@id='days']    1
    Select From List By Index    //*[@id='months']    1
    Select From List By Index    //*[@id='years']    1
    Check Checkbox    //*[@id='newsletter']
    Check Checkbox    //*[@id='optin']
    Input Text    //*[@id='first_name']    ${FIRST_NAME}
    Input Text    //*[@id='last_name']    ${LAST_NAME}
    Input Text    //*[@id='company']    ${COMPANY}
    Input Text    //*[@id='address1']    ${ADDRESS1}
    Input Text    //*[@id='address2']    ${ADDRESS2}
    Select From List    //*[@id='country']    ${COUNTRY}
    Input Text    //*[@id='state']    ${STATE}
    Input Text    //*[@id='city']    ${CITY}
    Input Text    //*[@id='zipcode']    ${ZIPCODE}
    Input Text    //*[@id='mobile_number']    ${MOBILE}
    Click Button    //*[@id='submitAccount']
    Element Should Be Visible    //h2[contains(text(), 'ACCOUNT CREATED!')]
    Click Link    Continue
    Element Should Be Visible    //*[contains(text(), 'Logged in as')]
    Click Button    //*[@id='deleteAccount']
    Element Should Be Visible    //h2[contains(text(), 'ACCOUNT DELETED!')]
    Close Browser