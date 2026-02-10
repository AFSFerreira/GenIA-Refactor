*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${LOGIN_URL}    http://localhost:5173/LogIn
${EMAIL}    incorrect@example.com
${PASSWORD}    wrongpassword

*** Test Cases ***
Unsuccessfully Login with Incorrect Credentials
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Home Page
    Click Link    xpath=//a[@href='/LogIn']
    Title Should Be    Log In
    Input Text    xpath=//*[@id='email']    ${EMAIL}
    Input Text    xpath=//*[@id='password']    ${PASSWORD}
    Click Button    xpath="//button[contains(text(), 'Log In')]"
    Element Should Be Visible    xpath="//*[contains(text(), 'User not found!')]"
    Close Browser