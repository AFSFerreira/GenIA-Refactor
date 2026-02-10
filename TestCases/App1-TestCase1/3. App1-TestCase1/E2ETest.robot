*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${EMAIL}    test@example.com

*** Test Cases ***
Verify Subscription in home page
    [Documentation]    Verify Subscription in home page
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Element Should Be Visible    xpath=//*[@id='slider-carousel']
    Scroll Down
    Element Should Be Visible    xpath=//*[contains(text(), 'SUBSCRIPTION')]
    Input Text    xpath=//*[@id='susbscribe_email']    ${EMAIL}
    Click Button    xpath=//*[@id='subscribe']
    Element Should Be Visible    xpath=//*[contains(text(), 'You have been successfully subscribed!')]
    Close Browser