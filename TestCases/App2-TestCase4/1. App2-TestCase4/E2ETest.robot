*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL_HOME}    http://localhost:5173/
${URL_MOVIE}   http://localhost:5173/MovieSession/
${MOVIE_TITLE}    Barbie
${MOVIE_CARD_XPATH}    //h4[contains(text(), '${MOVIE_TITLE}')]

*** Test Cases ***
Test Case 4: Successfully Navigate to Movie Details Page
    [Documentation]    This test case verifies the navigation to the movie details page for 'Barbie'.
    Open Browser    ${URL_HOME}    chrome
    Maximize Browser Window
    Title Should Be    Home
    Click Element    ${MOVIE_CARD_XPATH}
    Wait Until Page Contains Element    //h1[contains(text(), '${MOVIE_TITLE}')]
    Title Should Be    ${MOVIE_TITLE}
    Close Browser