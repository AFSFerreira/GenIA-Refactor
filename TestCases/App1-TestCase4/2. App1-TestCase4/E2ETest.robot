*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${CART_URL}    https://automationexercise.com/view_cart
${EMAIL}    test@example.com

*** Test Cases ***
Verify Subscription in Cart page
    [Documentation]    Verify that the subscription functionality works correctly on the cart page.
    Launch Browser    Chrome
    Go To    ${URL}
    Title Should Be    Automation Exercise
    Click Element    //a[contains(text(), 'Cart')]
    Go To    ${CART_URL}
    Scroll Down
    Element Should Be Visible    //*[contains(text(), 'SUBSCRIPTION')]
    Input Text    //*[@id='susbscribe_email']    ${EMAIL}
    Click Element   //*[@id='subscribe']
    Element Should Be Visible    //*[contains(text(), 'You have been successfully subscribed!')]
    Close Browser