*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${STATE_DROPDOWN}    xpath=//*[@id='estado-dropdown']
${STATE_OPTION}    xpath=//*[@id='estado-dropdown']/option[text()='AM']
${MOVIE_CARD}    xpath=//*[contains(text(), 'Joker')]

*** Test Cases ***
Test Case 6: Successfully Filter Movies by State
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Home Page
    Click Element    ${STATE_DROPDOWN}
    Click Element    ${STATE_OPTION}
    Element Should Be Visible    ${MOVIE_CARD}
    Close Browser