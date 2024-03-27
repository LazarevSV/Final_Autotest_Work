from testpage import OperationsHelper, get, post, get_post, login
import logging
import time
import yaml
from nikto_data import *

with open('testdata.yaml') as f:
    test_data = yaml.safe_load(f)

#Step 1: Login with invalid data
def test_step_1(browser):
    logging.info("Test 1 starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login('test')
    testpage.enter_pass('test')
    testpage.click_login_button()
    assert testpage.get_error_text() == str(test_data['login_error'])

# Step 2: Login with valid data
def test_step_2(browser):
    logging.info("Test 2 starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(test_data['login'])
    testpage.enter_pass(test_data['password'])
    testpage.click_login_button()
    assert testpage.get_login_enter_text() == test_data['login_word']

# Step 3: Press 'About' button and check page title
def test_step_3(browser):
    logging.info("Test 3 starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(test_data['login'])
    testpage.enter_pass(test_data['password'])
    testpage.click_login_button()

    testpage.click_about_button()
    time.sleep(test_data['sleep_time'])
    assert testpage.get_about_text() == test_data['about_title']



## Step 4: Check front size in page title
def test_step4(browser):

    logging.info("Test 4 starting")
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login(test_data['login'])
    testpage.enter_pass(test_data['password'])
    testpage.click_login_button()

    testpage.click_about_button()
    time.sleep(test_data['sleep_time'])
    assert testpage.take_title_font_size() == test_data["font_size"]



def test_step_5():
    logging.info("Test 4 starting")
    # nikto data
    cmd_name = test_data["cmd_name"]
    cmd_h_key = test_data["cmd_h_key"]
    site_url = test_data["site_url"]
    ssl_key = test_data["ssl_key"]
    tuning_key = test_data["tuning_key"]
    tuning_level_value = test_data["tuning_level_value"]
    cmd_o_key = test_data["cmd_o_key"]
    output_file_url = test_data['output_file_url']

    # Valid data
    zero_errors = test_data['zero_errors']

    run_process(
        f'{cmd_name} {cmd_h_key} {site_url} {ssl_key} {tuning_key} {tuning_level_value} {cmd_o_key} {output_file_url}')
    flag = find_words_in_file(output_file_url, zero_errors)
    assert flag