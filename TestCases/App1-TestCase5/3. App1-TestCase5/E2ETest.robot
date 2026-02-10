*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${NAME}    Test User
${EMAIL}   testuser@example.com
${PASSWORD}    TestPassword123
${FIRSTNAME}    Test
${LASTNAME}    User
${COMPANY}    Test Company
${ADDRESS1}    123 Test St
${ADDRESS2}    Apt 4
${COUNTRY}    United States
${STATE}    California
${CITY}    Test City
${ZIPCODE}    12345
${MOBILE}    1234567890

*** Test Cases ***
Register User
    Open Browser    ${URL}    Chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Click Element    xpath=//*[@id='header']/div[2]/div/div/nav/div[1]/a
    Element Should Be Visible    xpath=//h2[contains(text(), 'New User Signup!')]
    Input Text    xpath=//input[@placeholder='Name']    ${NAME}
    Input Text    xpath=//input[@placeholder='Email']    ${EMAIL}
    Click Element    xpath=//button[contains(text(), 'Signup')]
    Element Should Be Visible    xpath=//*[contains(text(), 'ENTER ACCOUNT INFORMATION')]
    Select Radio Button    xpath=//*[@id='id_gender']    Mr.
    Input Text    xpath=//*[@id='customer_firstname']    ${FIRSTNAME}
    Input Text    xpath=//*[@id='email']    ${EMAIL}
    Input Text    xpath=//*[@id='passwd']    ${PASSWORD}
    Select From List By Index    xpath=//*[@id='days']    1
    Select From List By Index    xpath=//*[@id='months']    1
    Select From List By Index    xpath=//*[@id='years']    1
    Click Element    xpath=//*[@id='newsletter']
    Click Element    xpath=//*[@id='optin']
    Input Text    xpath=//*[@id='firstname']    ${FIRSTNAME}
    Input Text    xpath=//*[@id='lastname']    ${LASTNAME}
    Input Text    xpath=//*[@id='company']    ${COMPANY}
    Input Text    xpath=//*[@id='address1']    ${ADDRESS1}
    Input Text    xpath=//*[@id='address2']    ${ADDRESS2}
    Select From List By Value    xpath=//*[@id='country']    ${COUNTRY}
    Input Text    xpath=//*[@id='state']    ${STATE}
    Input Text    xpath=//*[@id='city']    ${CITY}
    Input Text    xpath=//*[@id='zipcode']    ${ZIPCODE}
    Input Text    xpath=//*[@id='mobile_number']    ${MOBILE}
    Click Element    xpath=//*[@id='submitAccount']
    Element Should Be Visible    xpath=//*[contains(text(), 'ACCOUNT CREATED!')]
    Click Element    xpath=//a[contains(text(), 'Continue')]
    Element Should Be Visible    xpath=//*[contains(text(), 'Logged in as')]
    Click Element    xpath=//*[@id='deleteAccount']
    Element Should Be Visible    xpath=//*[contains(text(), 'ACCOUNT DELETED!')]
    Close Browser