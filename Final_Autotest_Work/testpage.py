import requests
import yaml
from BaseApp import BasePage
from selenium.webdriver.common.by import By
import logging

with open('testdata.yaml') as f:
    test_data = yaml.safe_load(f)
    browser = test_data['browser']


class TestSearchLocators:
    ids = dict()
    with open("./locators.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators['xpath'].keys():
        ids[locator] = (By.XPATH, locators['xpath'][locator])
    for locator in locators['css'].keys():
        ids[locator] = (By.CSS_SELECTOR, locators['css'][locator])


class OperationsHelper(BasePage):

    def enter_text_into_field(self, locator, word, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        logging.debug(f'Send {word} to element {element_name}')
        field = self.find_element(locator)
        if not field:
            logging.error(f'Element {locator} not found')
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.exception(f'Exception while operation with {locator}')
            return False
        return True

    def click_button(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.exception('Exception with click')
            return False
        logging.debug(f'Clicked {element_name} buttton')
        return True

    def take_css_property(self, locator, property):
        field = self.get_element_property(locator, property)
        return field

    def get_text_from_element(self, locator, description=None):
        if description:
            element_name = description
        else:
            element_name = locator
        field = self.find_element(locator, time=3)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.exception(f'Exception while get test from {element_name}')
            return None
        logging.debug(f'We find text {text} in field {element_name}')
        return text



    # ENTER TEXT
    def enter_login(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_LOGIN_FIELD'], word,
                                   description='login form')

    def enter_pass(self, word):
        self.enter_text_into_field(TestSearchLocators.ids['LOCATOR_PASS_FIELD'], word,
                                   description='password form')

    def click_login_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_LOGIN_BTN'], description='Login button')

    def click_about_button(self):
        self.click_button(TestSearchLocators.ids['LOCATOR_ABOUT_BUTTON'], description='About button')

    def get_error_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ERROR_FIELD'], description='error 401')

    def get_login_enter_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_LOGIN_ENTER'], description='login text')

    def get_about_text(self):
        return self.get_text_from_element(TestSearchLocators.ids['LOCATOR_ABOUT_TITTLE'], description='about tittle')


    def take_title_font_size(self):
        return self.take_css_property(TestSearchLocators.ids['LOCATOR_ABOUT_TITTLE'], 'font-size')

def login():
    try:
        response = requests.post(test_data['url_login'],
                                 data={'username': test_data['login_1'], 'password': test_data['password_1']})
        if response.status_code == 200:
            return response.json()['token']
        else:
            logging.error(f"Error login. Status code: {response.status_code}")
            return None
    except:
        logging.exception(f"Exception with login")
        return None


def get(token):
    try:
        resource = requests.get(test_data['url_posts'],
                                headers={'X-Auth-Token': token},
                                params={'owner': 'notMe'})
        if resource.status_code == 200:
            return resource.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resource.status_code}")
            return None
    except:
        logging.exception(f"Exception with get")
        return None


def post(token):
    try:
        new_post = requests.post(test_data['url_posts'],
                                 data={'title': "Writer",
                                       'description': "Pushkin",
                                       'content': "A.S.Pushkin"},
                                 headers={'X-Auth-Token': token})
        if new_post.status_code == 200:
            return new_post.json()
        else:
            logging.error(f"Error with posting data. Status code: {new_post.status_code}")
            return None
    except:
        logging.exception(f"Exception with post")
        return None


def get_post(token):
    try:
        resource = requests.get(test_data['url_posts'],
                                headers={'X-Auth-Token': token})
        if resource.status_code == 200:
            return resource.json()
        else:
            logging.error(f"Error with retrieving data. Status code: {resource.status_code}")
            return None
    except:
        logging.exception(f"Exception with get_post")
        return None