#!/usr/bin/env python3
"""
Twitter Interest Cleaner
A script to automatically disable all Twitter interests for a cleaner, ad-free experience.

Usage:
    python twitter_cleaner.py --config config.json
    python twitter_cleaner.py --manual  # For manual token input
    python twitter_cleaner.py --help
"""

import json
import requests
import argparse
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_cleaner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TwitterCredentials:
    """Store Twitter API credentials"""
    bearer_token: str
    csrf_token: str
    auth_token: str  # From cookies
    ct0: str  # From cookies (CSRF token value)

class TwitterInterestCleaner:
    """Main class for cleaning Twitter interests"""
    
    def __init__(self, credentials: TwitterCredentials):
        self.credentials = credentials
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup HTTP session with essential headers and cookies only"""
        # Set essential cookies only
        self.session.cookies.set('auth_token', self.credentials.auth_token)
        self.session.cookies.set('ct0', self.credentials.ct0)
        
        # Set minimal required headers
        self.session.headers.update({
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {self.credentials.bearer_token}',
            'origin': 'https://x.com',
            'referer': 'https://x.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'x-csrf-token': self.credentials.csrf_token,
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en'
        })
    
    def get_current_interests(self) -> List[str]:
        """Fetch currently followed interests"""
        url = 'https://api.x.com/1.1/account/personalization/twitter_interests.json'
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            interests = [item['id'] for item in data.get('interested_in', [])]
            
            logger.info(f"Found {len(interests)} current interests")
            return interests
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch current interests: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            raise
    
    def get_disabled_interests(self) -> List[str]:
        """Fetch currently disabled interests"""
        url = 'https://api.x.com/1.1/account/personalization/p13n_preferences.json'
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            disabled = data.get('interest_preferences', {}).get('disabled_interests', [])
            
            logger.info(f"Found {len(disabled)} already disabled interests")
            return disabled
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch disabled interests: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            raise
    
    def disable_all_interests(self, all_interests: List[str]) -> bool:
        """Disable all interests (current + already disabled)"""
        url = 'https://api.x.com/1.1/account/personalization/p13n_preferences.json'
        
        payload = {
            "preferences": {
                "interest_preferences": {
                    "disabled_interests": all_interests,
                    "disabled_partner_interests": []
                }
            }
        }
        
        # Add content-type header for POST request
        headers = {'content-type': 'application/json'}
        
        try:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.info(f"Successfully disabled {len(all_interests)} interests")
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to disable interests: {e}")
            return False
    
    def clean_interests(self) -> bool:
        """Main method to clean all Twitter interests"""
        logger.info("Starting Twitter interest cleaning process...")
        
        try:
            # Step 1: Get current interests
            current_interests = self.get_current_interests()
            
            # Step 2: Get already disabled interests
            disabled_interests = self.get_disabled_interests()
            
            # Step 3: Combine and deduplicate
            all_interests = list(set(current_interests + disabled_interests))
            
            logger.info(f"Total unique interests to disable: {len(all_interests)}")
            
            # Step 4: Disable all interests
            success = self.disable_all_interests(all_interests)
            
            if success:
                logger.info("✅ Successfully cleaned all Twitter interests!")
                return True
            else:
                logger.error("❌ Failed to clean interests")
                return False
                
        except Exception as e:
            logger.error(f"Error during cleaning process: {e}")
            return False

def load_config(config_path: str) -> Optional[TwitterCredentials]:
    """Load credentials from config file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return TwitterCredentials(
            bearer_token=config['bearer_token'],
            csrf_token=config['csrf_token'],
            auth_token=config['auth_token'],
            ct0=config['ct0']
        )
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        return None
    except KeyError as e:
        logger.error(f"Missing required field in config: {e}")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid JSON in config file")
        return None

def create_sample_config():
    """Create a sample config file"""
    sample_config = {
        "bearer_token": "YOUR_BEARER_TOKEN_HERE",
        "csrf_token": "YOUR_CSRF_TOKEN_HERE", 
        "auth_token": "YOUR_AUTH_TOKEN_FROM_COOKIES",
        "ct0": "YOUR_CT0_VALUE_FROM_COOKIES"
    }
    
    with open('config_sample.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("✅ Sample config created as 'config_sample.json'")
    print("📝 Please edit this file with your actual tokens:")
    print("   • bearer_token: From Authorization header (without 'Bearer ')")
    print("   • csrf_token: From x-csrf-token header")
    print("   • auth_token: From auth_token cookie")
    print("   • ct0: From ct0 cookie (usually same as csrf_token)")
    print("💡 Rename to 'config.json' when ready")

def manual_input() -> TwitterCredentials:
    """Get credentials via manual input"""
    print("🔐 Manual Token Input Mode")
    print("Please enter the 4 essential tokens:")
    
    bearer_token = input("Bearer Token (from Authorization header): ").strip()
    csrf_token = input("CSRF Token (from x-csrf-token header): ").strip()
    auth_token = input("Auth Token (from auth_token cookie): ").strip()
    ct0 = input("CT0 (from ct0 cookie, usually same as CSRF): ").strip()
    
    # Auto-fill ct0 if empty
    if not ct0:
        ct0 = csrf_token
        print(f"ℹ️  Using CSRF token value for ct0: {ct0[:20]}...")
    
    return TwitterCredentials(
        bearer_token=bearer_token,
        csrf_token=csrf_token,
        auth_token=auth_token,
        ct0=ct0
    )

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Clean all Twitter interests for a better experience",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python twitter_cleaner.py --config config.json
  python twitter_cleaner.py --manual
  python twitter_cleaner.py --create-config
        """
    )
    
    parser.add_argument('--config', '-c', help='Path to config file with tokens')
    parser.add_argument('--manual', '-m', action='store_true', help='Enter tokens manually')
    parser.add_argument('--create-config', action='store_true', help='Create sample config file')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be disabled without making changes')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Get credentials
    credentials = None
    
    if args.config:
        credentials = load_config(args.config)
    elif args.manual:
        credentials = manual_input()
    else:
        # Try default config file
        if os.path.exists('config.json'):
            credentials = load_config('config.json')
        else:
            print("❌ No config file found and no manual input specified")
            print("💡 Use --create-config to create a sample config file")
            print("💡 Or use --manual to enter tokens manually")
            sys.exit(1)
    
    if not credentials:
        print("❌ Failed to load credentials")
        sys.exit(1)
    
    # Run the cleaner
    cleaner = TwitterInterestCleaner(credentials)
    
    if args.dry_run:
        print("🔍 Dry run mode - showing what would be disabled...")
        try:
            current = cleaner.get_current_interests()
            disabled = cleaner.get_disabled_interests()
            total = list(set(current + disabled))
            
            print(f"📊 Summary:")
            print(f"  - Current interests: {len(current)}")
            print(f"  - Already disabled: {len(disabled)}")
            print(f"  - Total to disable: {len(total)}")
            
        except Exception as e:
            logger.error(f"Error during dry run: {e}")
            sys.exit(1)
    else:
        success = cleaner.clean_interests()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()