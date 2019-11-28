# ============================================================================
# ADD BANDO ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rer.bandi -t test_add_bando.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rer.bandi.testing.RER_BANDI_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/rer/bandi/tests/robot/test_add_bando.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test cases ***************************************************************

Scenario: Required fields when adding new bando
    Given a logged-in site administrator
        and an add Bando form
    When I submit the form
    Then required fields have errors

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator  Contributor  Reviewer

an add Bando form
  Go To  ${PLONE_URL}/++add++Bando

# --- When -------------------------------------------------------------------

I submit the form
  Click Button  Save

# --- Then -------------------------------------------------------------------

required fields have errors
  Wait until page contains  Site Map
  Page should contain  There were some errors.
  Page should contain Element  css=div#formfield-form-widgets-tipologia_bando.error
  Page should contain Element  css=div#formfield-form-widgets-destinatari.error
