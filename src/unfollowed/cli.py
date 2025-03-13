"""
CLI for the unfollowed bot.

This module initializes and runs the unfollowed bot based on the CLI options.
The bot logs into Instagram, collects the list of followers and following,
computes users who don't follow you back, and displays the results.

Usage:
    uv run uf --config <path_to_config> --profile <profile_name> [--allowlist] [--log-level <log_level>]
"""

import logging

import click

from unfollowed.bot import Bot
from unfollowed.constants import LOG_LEVELS
from unfollowed.utils import (
    get_credentials,
    load_allowlist,
    users_that_dont_follow_you_back,
    users_you_dont_follow_back,
    write_to_disk,
)

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "-c",
    "--config",
    required=True,
    help="Path to required config.ini file",
)
@click.option(
    "-p",
    "--profile",
    required=True,
    help="Section name in config.ini containing `username` and `password` fields of the account",
)
@click.option(
    "-a",
    "--allowlist",
    is_flag=True,
    help="Tells the bot to look inside the config.ini profile for a key `allowlist` with a JSON list of accounts you expect to not follow you",
)
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(list(LOG_LEVELS.keys()), case_sensitive=False),
    default="info",
    show_default=True,
    help="Set the logging level",
)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(writable=True),
    help="Path to the output file.",
)
def run(
    config: str, profile: str, allowlist: bool, log_level: str, output_file: str
) -> None:
    """
    Run the unfollowed bot with the specified configuration.

    This function configures logging, retrieves the Instagram credentials and optional allowlist
    from the provided configuration file, initializes and runs the bot to collect followers and following,
    computes the unfollowed results, and prints the outcome to the console.

    Args:
        config (str): Path to the required config.ini file.
        profile (str): Section name in config.ini containing the 'username' and 'password' fields.
        allowlist (bool): If True, load an allowlist of accounts to ignore from the config.ini file.
        log_level (str): The logging level (must be one of the keys in LOG_LEVELS).
        output_file (str): Path to the output file

    Returns:
        None
    """
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] - %(message)s", level=LOG_LEVELS[log_level]
    )

    logger.info("Starting uf")

    username, password = get_credentials(config, profile)

    allowed_users = load_allowlist(config, profile) if allowlist else []
    logger.debug(allowed_users)

    logger.info("Initializing the bot")
    bot = Bot(username, password)
    logger.info("Successfully Initialized the bot")

    logger.info("Starting the bot")
    bot.run()
    logger.info("Finished running the bot")

    logger.info("Computing results")
    you_do_not_follow_back = users_you_dont_follow_back(bot.followers, bot.following)
    does_not_follow_you_back = users_that_dont_follow_you_back(
        bot.followers, bot.following, allowed_users
    )

    print("Users that don't follow you back:")
    print(*does_not_follow_you_back, sep="\n")
    print()
    print("Users that you don't follow back:")
    print(*you_do_not_follow_back, sep="\n")

    if output_file is not None:
        logger.info(f"Writing results to {output_file}")
        write_to_disk(output_file, you_do_not_follow_back, does_not_follow_you_back)
    else:
        logger.info("No output file specified, skipping write to disk")

    logger.info("Completed running")
