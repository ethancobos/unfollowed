"""Global constants."""

import logging

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
WEB_DRIVER_WAIT_TIME = 5

# Instagram CSS and Xpaths
CLOSE_BUTTON_CSS = '[aria-label="Close"]'
FOLLOWERS_CSS = '[href*="{username}/followers/"]'
SCROLL_BOX_CSS = '[class*="xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6"]'
FOLLOWING_CSS = '[href*="{username}/following/"]'
INSTAGRAM_URL = "https://www.instagram.com/accounts/login/"
NOTIFICATIONS_XPATH = "//button[contains(text(), 'Not Now')]"
PROFILE_CSS = '[href*="{username}"]'
SECOND_SAVE_LOGIN_INFO_XPATH = "//button[contains(text(), 'Save info')]"
SCROLL_BOX_USER_CSS = '[class*="_ap3a _aaco _aacw _aacx _aad7 _aade"]'

# Javascript
SCROLL_JS = """
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """
