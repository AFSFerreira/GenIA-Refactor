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
    Maximize Browser Window
    Title Should Be    Home Page
    Click Element    ${CREATE_MOVIE_BUTTON}
    Go To    ${CREATE_MOVIE_URL}
    Input Text    xpath=//input[@id='url_cartaz']    http://example.com/movie
    Input Text    xpath=//input[@id='nome']    Example Movie
    Input Text    xpath=//textarea[@id='descricao']    This is an example movie description.
    Input Text    xpath=//input[@id='faixa_etaria']    12
    Input Text    xpath=//input[@id='diretor']    John Doe
    Input Text    xpath=//input[@id='escritor']    Jane Doe
    Input Text    xpath=//input[@id='ator']    Actor Name
    Input Text    xpath=//input[@id='genero']    Action
    Input Text    xpath=//input[@id='data_lancamento']    2023-10-01
    Click Element    ${CRIAR_BUTTON}
    Page Should Contain    Film Created Successfully!
    Close Browser