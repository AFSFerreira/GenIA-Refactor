*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${CART_URL}    https://automationexercise.com/view_cart
${EMAIL}    test@example.com

*** Test Cases ***
Verify Subscription in Cart page
    [Documentation]    Verify that the subscription functionality works correctly on the cart page.
    Launch Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Automation Exercise
    Click Element    xpath=//*[@id='header']/div[2]/div/div[3]/div/a
    Go To    ${CART_URL}
    Scroll Down
    Element Should Be Visible    xpath=//*[contains(text(), 'SUBSCRIPTION')]
    Input Text    xpath="//input[@type='email']"    ${EMAIL}
    Click Element    xpath="//button[contains(@class, 'btn')]"
    Element Should Be Visible    xpath=//*[contains(text(), 'You have been successfully subscribed!')]
    Close Browser