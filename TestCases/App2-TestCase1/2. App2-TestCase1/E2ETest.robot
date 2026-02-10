*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${SEARCH_URL}    http://localhost:5173/search
${MOVIE_NAME}    Interstellar

*** Test Cases ***
Successfully Search for a Movie
    [Documentation]    Test case to search for a movie and verify the results.
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Title Should Be    Home
    Input Text    xpath=//*[@id='search_input']    ${MOVIE_NAME}
    Click Element    xpath=//*[@id='search_input']
    Press Key    xpath=//*[@id='search_input']    ENTER
    Go To    ${SEARCH_URL}
    Page Should Contain Element    //h1[contains(text(), '${MOVIE_NAME}')]
    Close Browser