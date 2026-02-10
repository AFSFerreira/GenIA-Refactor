*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${SEARCH_URL}    http://localhost:5173/search
${MOVIE_NAME}    Interstellar

*** Test Cases ***
Successfully Search for a Movie
    Open Browser    ${URL}    Chrome
    Maximize Browser Window
    Title Should Be    Home
    Input Text    xpath=//*[@id='search_input']    ${MOVIE_NAME}
    Click Element    xpath=//*[@id='search_input']
    Press Key    xpath=//*[@id='search_input']    ENTER
    Go To    ${SEARCH_URL}
    Element Should Be Visible    xpath=//h1[contains(text(), '${MOVIE_NAME}')] 
    Close Browser