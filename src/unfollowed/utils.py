"""Contains useful helper code for this project."""

import configparser
import json
import logging
import random
import sys
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from unfollowed.constants import SCROLL_JS, WEB_DRIVER_WAIT_TIME

logger = logging.getLogger(__name__)


def users_that_dont_follow_you_back(
    followers: list[str], following: list[str], allowlist: list[str]
) -> list[str]:
    """
    Identify users that don't follow you back, excluding those in the allowlist.

    Args:
        followers (list[str]): List of your followers.
        following (list[str]): List of users you follow.
        allowlist (list[str]): List of users to exclude from the results.

    Returns:
        list[str]: List of users that don't follow you back.
    """
    return list(set(following) - set(followers) - set(allowlist))


def users_you_dont_follow_back(followers: list[str], following: list[str]) -> list[str]:
    """
    Identify users that you don't follow back.

    Args:
        followers (list[str]): List of your followers.
        following (list[str]): List of users you follow.

    Returns:
        list[str]: List of users you don't follow back.
    """
    return list(set(followers) - set(following))


def human_wait() -> None:
    """Simulate human-like delay by sleeping for a random interval between 1 and 3 seconds."""
    logger.info("Waiting...")
    time.sleep(random.uniform(1, 3))
    logger.info("Done waiting")


def scroll(driver: WebDriver, scroll_box: WebElement) -> None:
    """
    Scroll to the bottom of a scrollable element.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        scroll_box (WebElement): Scrollable element.
    """
    last_ht, ht = 0, 1
    while last_ht != ht:
        last_ht = ht
        time.sleep(2.5)
        ht = driver.execute_script(
            SCROLL_JS,
            scroll_box,
        )
    time.sleep(2)


def load_allowlist(config_path: str, profile: str) -> list[str]:
    """
    Load the allowlist from a configuration file.

    Args:
        config_path (str): Path to the configuration file.
        profile (str): Profile name in the configuration file.

    Returns:
        list[str]: List of usernames in the allowlist.
    """
    try:
        logger.info("Attempting to retrieve allowlist")
        config = configparser.ConfigParser()
        config.read(config_path)
        items: list[str] = json.loads(config[profile]["allowlist"])
    except KeyError as e:
        logger.error(f"Configuration key error when attempting to load allowlist: {e}")
        sys.exit(1)

    logger.info("Successfully retrieved allowlist")
    return items


def get_credentials(config_path: str, profile: str) -> tuple[str, str]:
    """
    Retrieve credentials from a configuration file.

    Args:
        config_path (str): Path to the configuration file.
        profile (str): Profile name in the configuration file.

    Returns:
        tuple[str, str]: A tuple containing the username and password.
    """
    try:
        logger.info("Attempting to retrieve credentials")
        config = configparser.ConfigParser()
        config.read(config_path)
        username = config[profile]["username"]
        password = config[profile]["password"]
    except KeyError as e:
        logger.error(f"Configuration key error when attempting to get credentials: {e}")
        sys.exit(1)

    logger.info("Successfully retrieved credentials")
    return username, password


def click_button_css(driver: WebDriver, css: str) -> None:
    """
    Click a button using its CSS selector.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        css (str): CSS selector for the button.
    """
    try:
        element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css))
        )
        logger.debug(f"Is element enabled?: {element.is_enabled()}")
        logger.debug(f"Is element displayed?: {element.is_displayed()}")
    except TimeoutException as e:
        logger.info(f"Timeout when looking for {css} with exception: {e}")
        logger.info(
            "Assuming this is a popup that might not show up all the time, contiuing script excecution"
        )
        return

    human_wait()

    element.click()


def click_button_xpath(driver: WebDriver, xpath: str) -> None:
    """
    Click a button using its XPath.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        xpath (str): XPath for the button.
    """
    try:
        element = WebDriverWait(driver, WEB_DRIVER_WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        logger.debug(f"Is element enabled?: {element.is_enabled()}")
        logger.debug(f"Is element displayed?: {element.is_displayed()}")
    except TimeoutException as e:
        logger.info(f"Timeout when looking for {xpath} with exception: {e}")
        logger.info(
            "Assuming this is a popup that might not show up all the time, contiuing script excecution"
        )
        return

    human_wait()

    element.click()


def write_to_disk(
    path: str, you_dont_follow_back: list[str], dont_follow_you_back: list[str]
) -> None:
    """
    Write users that don't follow you back and users you don't follow back to a file.

    Args:
        path (str): Path to the output file.
        you_dont_follow_back (list[str]): List of users you don't follow back.
        dont_follow_you_back (list[str]): List of users that don't follow you back.
    """
    with open(path, "a") as file:
        file.write("*******Users that don't follow you back*******\n")
        file.write("\n".join(dont_follow_you_back) + "\n")
        file.write("*******Users that you don't follow back*******\n")
        file.write("\n".join(you_dont_follow_back) + "\n")
