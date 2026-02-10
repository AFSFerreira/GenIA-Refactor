*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL_HOME}    http://localhost:5173/
${URL_MOVIE}   http://localhost:5173/MovieSession/
${MOVIE_CARD}  //img[contains(@src, 'p13472534_p_v12_ah.jpg')]
${LOGO}        //*[@src='http://localhost:5173/src/assets/infeed_logo.svg']

*** Test Cases ***
Test Case 4: Successfully Navigate to Movie Details Page
    Open Browser    ${URL_HOME}    chrome
    Maximize Browser Window
    Title Should Be    Home
    Element Should Be Visible    ${LOGO}
    Click Element    ${MOVIE_CARD}
    Go To    ${URL_MOVIE}
    Title Should Be    Barbie
    Close Browser