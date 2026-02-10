*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://localhost:5173/
${CREATE_MOVIE_BUTTON}    xpath=//*[@id='createMovieButton']
${CRIAR_BUTTON}    xpath=//*[@id='criar_button']

*** Test Cases ***
Successfully Register a New Movie
    [Documentation]    Test case to register a new movie successfully.
    Open Browser    ${URL}    chrome
    Title Should Be    Home Page
    Click Button    ${CREATE_MOVIE_BUTTON}
    Go To    ${URL}CreateMovie
    Input Text    xpath=//input[@id='cartaz']    http://example.com/cartaz
    Input Text    xpath=//input[@id='nome']    Example Movie
    Input Text    xpath=//textarea[@id='descricao']    This is an example movie description.
    Input Text    xpath=//input[@id='faixa_etaria']    12
    Input Text    xpath=//input[@id='diretor']    John Doe
    Input Text    xpath=//input[@id='escritor']    Jane Doe
    Input Text    xpath=//input[@id='ator']    Actor Name
    Input Text    xpath=//input[@id='genero']    Action
    Input Text    xpath=//input[@id='data_lancamento']    2023-10-01
    Click Button    ${CRIAR_BUTTON}
    Page Should Contain    Film Created Successfully!
    Close Browser