"""Webscraping engine."""

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from unfollowed.constants import (
    CLOSE_BUTTON_CSS,
    FOLLOWERS_CSS,
    FOLLOWING_CSS,
    INSTAGRAM_URL,
    NOTIFICATIONS_XPATH,
    PROFILE_CSS,
    SCROLL_BOX_CSS,
    SCROLL_BOX_USER_CSS,
    SECOND_SAVE_LOGIN_INFO_XPATH,
    WEB_DRIVER_WAIT_TIME,
)
from unfollowed.utils import click_button_css, click_button_xpath, human_wait, scroll

logger = logging.getLogger(__name__)


class Bot:
    """Navigates through instagram and webscrapes all of the data."""

    def __init__(self, username: str, password: str):
        """
        Initializes the Bot with the given username and password.

        Args:
            username (str): The Instagram username.
            password (str): The Instagram password.
        """
        self.username = username
        self.password = password
        self.followers: list[str] = []
        self.following: list[str] = []
        self.driver: WebDriver

    def run(self) -> None:
        """Runs the bot through the complete sequence of operations."""
        logger.info("Running the bot")

        # goto Instagram
        self.open_instagram()

        # attempt to login
        self.login()

        # bypass the first 'save login info' pop up
        self.bypass_first_save_login_info_popup()

        # bypass the second 'save login info' pop up
        self.bypass_second_save_login_info_popup()

        # bypass the 'turn on notifications pop up'
        self.bypass_notifications_popup()

        # navigate to profile
        self.navigate_to_profile()

        # get all followers, store in self.followers
        self.get_followers()

        # get entire following, store in self.following
        self.get_following()

        # exit Instagram
        self.exit_instagram()

        logger.info("Finished running the bot")

    def open_instagram(self) -> None:
        """Opens Instagram in a web browser."""
        logger.info("Opening Chrome")
        self.driver = webdriver.Chrome()
        logger.info("Successfully Opened Chrome")

        human_wait()

        logger.info("Connecting to Instagram")
        self.driver.get(INSTAGRAM_URL)
        logger.info("Successfully connected to Instagram")

    def login(self) -> None:
        """Logs into Instagram using the provided credentials."""
        logger.info("Attempting to enter username")
        username_field = WebDriverWait(self.driver, WEB_DRIVER_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        human_wait()

        username_field.send_keys(self.username)
        logger.info("Username entered successfully")

        logger.info("Attempting to enter password")
        password_field = WebDriverWait(self.driver, WEB_DRIVER_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        human_wait()

        # This is really strange, after entering the first character of the
        # password field, the cursor jumps back to the username field
        # we need to bypass this behavior by first entering the first character
        # then entering the rest of the password
        password_field.send_keys(str(self.password[0]))
        password_field.send_keys(self.password[1:])

        human_wait()

        password_field.send_keys("\ue007")
        logger.info("Password entered successfully")
        logger.info("Successfully logged in")

    def bypass_first_save_login_info_popup(self) -> None:
        """
        Closes the first 'Save Login Info' popup on Instagram.

        Note: this popup may or may not be present, if not the bot should continue
              on with no issue.
        """
        logger.info("Attempting to bypass the save login info popup")
        click_button_css(self.driver, CLOSE_BUTTON_CSS)
        logger.info("Successfully bypasses the save login info popup")

    def bypass_second_save_login_info_popup(self) -> None:
        """
        Closes the second 'Save Login Info' popup on Instagram.

        Note: this popup may or may not be present, if not the bot should continue
              on with no issue.
        """
        logger.info("Attempting to bypass the save login info popup")
        click_button_xpath(self.driver, SECOND_SAVE_LOGIN_INFO_XPATH)
        logger.info("Successfully bypasses the save login info popup")

    def bypass_notifications_popup(self) -> None:
        """
        Closes the 'Turn on Notifications' popup on Instagram.

        Note: this popup may or may not be present, if not the bot should continue
              on with no issue.
        """
        logger.info("Attempting to bypass the notifications popup")
        click_button_xpath(self.driver, NOTIFICATIONS_XPATH)
        logger.info("Successfully bypasses the notifications popup")

    def navigate_to_profile(self) -> None:
        """Navigates to the user's Instagram profile page."""
        logger.info("Attempting to navigate to the use profile")
        formatted_CSS = PROFILE_CSS.format(username=self.username)
        logger.debug(f"using CSS string: {formatted_CSS}")
        click_button_css(self.driver, formatted_CSS)
        logger.info("Successfully navigate to the user profile")

    def get_followers(self) -> None:
        """Retrieves the list of followers and stores them in self.followers."""
        logger.info("Attempting to collect all followers")
        # open followers dialog
        formatted_CSS = FOLLOWERS_CSS.format(username=self.username)
        logger.debug(f"using CSS string: {formatted_CSS}")
        click_button_css(self.driver, formatted_CSS)

        human_wait()

        # find the scroll box and scroll to the bottom
        scroll_box = WebDriverWait(self.driver, WEB_DRIVER_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SCROLL_BOX_CSS))
        )

        human_wait()

        logger.info("Scrolling...")
        scroll(self.driver, scroll_box)

        human_wait()

        # collect all of the user once we've loaded them all in through scrolling
        list_elems = scroll_box.find_elements(
            by=By.CSS_SELECTOR, value=SCROLL_BOX_USER_CSS
        )

        # store in class attribute
        self.followers = [elem.text for elem in list_elems]
        logger.info(f"Successfully found {len(self.followers)} followers")

        # close out of followers dialog
        click_button_css(self.driver, CLOSE_BUTTON_CSS)
        logger.info("Successfully closed out of followers dialog")

    def get_following(self) -> None:
        """Retrieves the list of accounts the user is following and stores them in self.following."""
        logger.info("Attempting to collect all followings")
        # open following dialog
        formatted_CSS = FOLLOWING_CSS.format(username=self.username)
        logger.debug(f"using CSS string: {formatted_CSS}")
        click_button_css(self.driver, formatted_CSS)

        human_wait()

        # find the scroll box and scroll to the bottom
        scroll_box = WebDriverWait(self.driver, WEB_DRIVER_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SCROLL_BOX_CSS))
        )

        human_wait()

        logger.info("Scrolling...")
        scroll(self.driver, scroll_box)

        # collect all of the user once we've loaded them all in through scrolling
        list_elems = scroll_box.find_elements(
            by=By.CSS_SELECTOR, value=SCROLL_BOX_USER_CSS
        )

        human_wait()

        # store in class attribute
        self.following = [elem.text for elem in list_elems]
        logger.info(f"Successfully found {len(self.following)} followings")

        # close out of followers dialog
        click_button_css(self.driver, CLOSE_BUTTON_CSS)
        logger.info("Successfully closed out of following dialog")

    def exit_instagram(self) -> None:
        """Closes the web driver and exits Instagram."""
        logger.info("Exiting Instagram")
        self.driver.quit()
        logger.info("Successfully exited Instagram")
