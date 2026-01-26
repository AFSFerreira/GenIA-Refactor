*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    http://automationexercise.com
${CONTACT_US_URL}    https://automationexercise.com/contact_us
${NAME}    Test User
${EMAIL}    testuser@example.com
${SUBJECT}    Test Subject
${MESSAGE}    This is a test message.
${FILE_PATH}    path/to/your/file.txt

*** Test Cases ***
Test Case 6: Contact Us Form
    Open Browser    ${URL}    Chrome
    Maximize Browser Window
    Go To    ${URL}
    Title Should Be    Automation Exercise
    Click Element    //a[contains(text(), 'Contact Us')]
    Go To    ${CONTACT_US_URL}
    Element Should Be Visible    //h2[contains(text(), 'Get In Touch')]
    Input Text    //*[@id='contact-us-form']//input[@name='name']    ${NAME}
    Input Text    //*[@id='contact-us-form']//input[@name='email']    ${EMAIL}
    Input Text    //*[@id='contact-us-form']//input[@name='subject']    ${SUBJECT}
    Input Text    //*[@id='contact-us-form']//textarea[@name='message']    ${MESSAGE}
    Choose File    //*[@id='contact-us-form']//input[@name='upload_file']    ${FILE_PATH}
    Click Element    //*[@id='contact-us-form']//input[@name='submit']
    Click Element    //button[contains(text(), 'OK')]
    Element Should Be Visible    //div[contains(text(), 'Success! Your details have been submitted successfully.')]
    Click Element    //a[contains(@href, '/') and contains(text(), 'Home')]
    Element Should Be Visible    //*[@class='nav navbar-nav']/li[1]/a
    Close Browser