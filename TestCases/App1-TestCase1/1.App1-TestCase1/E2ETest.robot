*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${EMAIL_INPUT}    xpath=//*[@id='susbscribe_email']
${SUBSCRIBE_BUTTON}    xpath=//*[@id='subscribe']
${SUCCESS_MESSAGE}    xpath=//*[contains(text(), 'You have been successfully subscribed!')]

*** Test Cases ***
Verify Subscription in home page
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Scroll Down
    Element Should Be Visible    ${SUCCESS_MESSAGE}
    Input Text    ${EMAIL_INPUT}    test@example.com
    Click Button    ${SUBSCRIBE_BUTTON}
    Element Should Be Visible    ${SUCCESS_MESSAGE}
    Close Browser