*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL_HOME}    http://localhost:5173/
${URL_MOVIE}   http://localhost:5173/MovieSession/
${MOVIE_TITLE}    Barbie
${LOGO_XPATH}    //*[@src='http://localhost:5173/src/assets/infeed_logo.svg']
${MOVIE_CARD_XPATH}    //*[contains(text(), '${MOVIE_TITLE}')]/ancestor::div[contains(@class, 'movie-card')]

*** Test Cases ***
Test Case 4: Successfully Navigate to Movie Details Page
    Open Browser    ${URL_HOME}    chrome
    Maximize Browser Window
    Title Should Be    Home
    Element Should Be Visible    ${LOGO_XPATH}
    Click Element    ${MOVIE_CARD_XPATH}
    Go To    ${URL_MOVIE}
    Title Should Be    ${MOVIE_TITLE} Details
    Close Browser