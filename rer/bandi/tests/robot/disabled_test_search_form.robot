# ============================================================================
# SEARCH FORM BANDI ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rer.bandi -t test_search_form.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rer.bandi.testing.RER_BANDI_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/rer/bandi/tests/robot/test_search_form.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Initialize test
Test Teardown  Close all browsers

*** Test cases ***************************************************************

Scenario: Search Bandi for Manifestazioni di interesse
    Given a logged-in contributor
    When I go to search_bandi_form view
        and search for 'Manifestazioni di interesse' type
    Then 'Bando 1' and 'Bando 2' appears as results, and not 'Bando 3'


*** Keywords *****************************************************************

Initialize test
    Open test browser
    Enable autologin as  Contributor
    Create Bando with title 'Bando 1' and 'Manifestazioni di interesse' type and 'PMI' destinatari and 'FESR' founds and 'Sport' topic
    Create Bando with title 'Bando 2' and 'Manifestazioni di interesse' type and 'Cittadini' destinatari and 'FESR' founds and 'Ambiente' topic
    Create Bando with title 'Bando 3' and 'Agevolazioni, finanziamenti, contributi' type and 'Enti del Terzo settore' destinatari and 'FESR' founds and 'Sport' topic
    Create Bando with title 'Bando 4' and 'Accreditamenti, albi, elenchi' type and 'PMI' destinatari and 'FESR' founds and 'Sport' topic

Create Bando with title '${title}' and '${tipologia_bando}' type and '${destinatari}' destinatari and '${finanziatori}' founds and '${materie}' topic
    Go To  ${PLONE_URL}/++add++Bando
    Input Text  id=form-widgets-IDublinCore-title  ${title}
    Select Radio button  form.widgets.tipologia_bando  ${tipologia_bando}
    Select Checkbox  xpath=//span[@id="form-widgets-destinatari"]/span/input[@value="${destinatari}"]
    Select Checkbox  xpath=//span[@id="form-widgets-finanziatori"]/span/input[@value="${finanziatori}"]
    Select Checkbox  xpath=//span[@id="form-widgets-materie"]/span/input[@value="${materie}"]
    Click Button  Save
    Page should contain  ${title}

# --- Given ------------------------------------------------------------------

a logged-in contributor
  Enable autologin as  Contributor

a logged-in manager
  Enable autologin as  Manager

# --- When -------------------------------------------------------------------

I go to search_bandi_form view
  Go To  ${PLONE_URL}/search_bandi_form

search for '${tipologia_bando}' type
    Wait until page contains  Site Map
    Select Checkbox  xpath=//input[@value="${tipologia_bando}"]
    Click Button  xpath=//form[@action="search_bandi"]/div/input[@value="Search"]


# --- Then -------------------------------------------------------------------

required fields have errors
  Wait until page contains  Site Map
  Page should contain  There were some errors.
  Page should contain Element  css=div#formfield-form-widgets-tipologia_bando.error
  Page should contain Element  css=div#formfield-form-widgets-destinatari.error

Then '${result1}' and '${result2}' appears as results, and not '${no_result}'
    Wait until page contains  Site Map
    Page should contain  ${result1}
    Page should contain  ${result2}
    Page should not contain  ${no_result}
