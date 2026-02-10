*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${CREATE_MOVIE_URL}    http://localhost:5173/CreateMovie
${CREATE_MOVIE_BUTTON}    xpath=//*[@id='createMovieButton']
${CRIAR_BUTTON}    xpath=//*[@id='criar_button']

*** Test Cases ***
Successfully Register a New Movie
    Open Browser    ${URL}    chrome
    Title Should Be    Home Page
    Click Button    ${CREATE_MOVIE_BUTTON}
    Go To    ${CREATE_MOVIE_URL}
    Fill In Movie Details
    Click Button    ${CRIAR_BUTTON}
    Page Should Contain    Film Created Successfully!
    Close Browser

*** Keywords ***
Fill In Movie Details
    [Documentation]    Fill in all required fields: url cartaz, nome, descrição, faixa etária, diretor(a), escritor(a), ator(a), gênero, and data de lançamento
    # Add the necessary input commands here to fill in the required fields.