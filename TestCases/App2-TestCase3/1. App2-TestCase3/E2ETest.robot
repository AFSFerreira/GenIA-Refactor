*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${LOGIN_URL}    http://localhost:5173/LogIn
${INCORRECT_EMAIL}    incorrect@example.com
${INCORRECT_PASSWORD}    wrongpassword

*** Test Cases ***
Unsuccessfully Login with Incorrect Credentials
    [Documentation]    Test case to verify unsuccessful login with incorrect credentials
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Home Page Title
    Click Link    xpath=//a[@href='/LogIn']
    Title Should Be    Log In Page Title
    Element Should Be Visible    xpath=//h1[contains(text(), 'Log In')]
    Input Text    xpath="//input[@type='email']"    ${INCORRECT_EMAIL}
    Input Text    xpath="//input[@type='password']"    ${INCORRECT_PASSWORD}
    Click Button    xpath="//button[contains(text(), 'Log In')]"
    Element Should Be Visible    xpath="//div[contains(text(), 'User not found!')]"
    Close Browser