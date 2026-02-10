*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${LOGIN_URL}    https://automationexercise.com/login
${INCORRECT_EMAIL}    incorrect@example.com
${INCORRECT_PASSWORD}    wrongpassword

*** Test Cases ***
Login User with incorrect email and password
    [Documentation]    Test case to login with incorrect credentials
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Click Element    xpath=//*[@id='header']/div[2]/div/div/nav/div[1]/a
    Wait Until Element Is Visible    xpath=//h2[contains(text(), 'Login to your account')]
    Input Text    xpath="//input[@type='email']"    ${INCORRECT_EMAIL}
    Input Text    xpath="//input[@type='password']"    ${INCORRECT_PASSWORD}
    Click Element    xpath="//button[contains(text(), 'Login')]"
    Wait Until Element Is Visible    xpath="//p[contains(text(), 'Your email or password is incorrect!')]"
    Close Browser