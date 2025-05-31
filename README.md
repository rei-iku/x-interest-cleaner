# X Interest Cleaner

> A tool to automatically disable all personalized interests on X (formerly Twitter).

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

X Interest Cleaner is a Python tool that automatically disables all X/Twitter interests that affect your personalized feed.

## Quick Start

### Prerequisites

- Python 3.7 or higher
- An X/Twitter account
- Basic command line knowledge

### Installation

1. Clone this repository:
```bash
git clone https://github.com/rei-iku/x-interest-cleaner.git
cd x-interest-cleaner
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Getting Your Authentication Tokens

You'll need to extract 4 tokens from your X session. We provide three methods:

### Method 1: Browser Console Script (Easiest)

1. Go to [x.com](https://x.com) and log in
2. Open Developer Tools (F12)
3. Go to the Console tab
4. Copy and paste the contents of `get_config_file.js`
5. Press Enter
6. A `config.json` file will be downloaded automatically

### Method 2: Bookmarklet

1. Open `index.html` in your browser
2. Drag the "Extract X Tokens" button to your bookmarks bar
3. Go to [x.com](https://x.com) and log in
4. Click the bookmark
5. Download the generated `config.json`

### Method 3: Manual Entry

Run the script with the `--manual` flag and enter tokens when prompted:
```bash
python x_interest_cleaner.py --manual
```

## Running the Script

Once you have your `config.json`:

```bash
# Run with config file
python x_interest_cleaner.py --config config.json

# Or if config.json is in the same directory
python x_interest_cleaner.py

# Preview what will be disabled (dry run)
python x_interest_cleaner.py --dry-run
```

## Command Line Options

```
usage: x_interest_cleaner.py [-h] [--config CONFIG] [--manual] [--create-config] [--dry-run]

Clean all X interests

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to config file with tokens
  --manual, -m          Enter tokens manually
  --create-config       Create sample config file
  --dry-run             Show what would be disabled without making changes
```

## Configuration

The `config.json` file needs these tokens:

```json
{
  "bearer_token": "AAAAAAAAAAAAAAAAAAAAAMLheAAA...",
  "csrf_token": "your_csrf_token_here",
  "ct0": "your_ct0_value_here",
}
```

## Troubleshooting

### "Could not find ct0 cookie"
- Make sure you're logged in to X
- Try refreshing the page
- Clear cookies and log in again

### "Failed to fetch interests"
- Your tokens may have expired
- Extract fresh tokens and try again

### Rate limiting
- X may temporarily block requests if you run the script too frequently
- Wait a few minutes and try again

## How It Works

1. **Authenticates** with X using your session tokens
2. **Fetches** all current interests from your account
3. **Retrieves** previously disabled interests
4. **Combines** both lists and removes duplicates
5. **Disables** all interests in a single API call

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not affiliated with X Corp. Use at your own risk. Make sure to comply with X's Terms of Service when using this tool.

## Acknowledgments

- Thanks to all contributors who help improve this tool