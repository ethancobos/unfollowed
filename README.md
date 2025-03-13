# Unfollowed

Unfollowed is a Python automation tool that logs into Instagram, retrieves your followers and following lists, and identifies users who don't follow you back and those you don't follow back. It also supports an allowlist to exclude specific accounts from the analysis.

## Installation

### Prerequisites
- Python 3.8+
- Google Chrome

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/unfollowed.git
   cd unfollowed
   ```
2. **Create a Virtual Environment**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```sh
   pip install click
   pip install selenium
   ```

## Usage

### Running the Bot
1. Ensure your Instagram credentials are set up in `config.ini` file like:
```
[john_doe]
username: foo
password: bar
```

2. Execute the bot:
   ```sh
   python -m main.py -c config.ini -p john_doe -o output.txt
   ```

The bot will:
- Open Instagram.
- Log in using provided credentials.
- Fetch your followers and following lists.
- Compute users who do not follow you back and those you do not follow.
- Print and optionally write the results to a file.

### Example Output
```plaintext
Users that don't follow you back:
1. user_one
2. user_two

Users that you don’t follow back:
1. user_three
2. user_four
```

### Project Structure
```
unfollowed/
├── README.md
├── main.py
├── pyproject.toml
├── src
│   └── unfollowed
│       ├── __init__.py
│       ├── bot.py
│       ├── cli.py
│       ├── constants.py
│       └── utils.py
└── uv.lock
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
Use the project at your own risk. Automating interactions with Instagram may violate their terms of service.


