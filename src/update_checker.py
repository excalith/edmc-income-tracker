"""
EDMC Income Tracker Plugin - Standalone version checking
"""

import requests # type: ignore
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

def check_for_updates(current_version, api_url):
    """
    Check if there's a newer version available on GitHub

    Args:
        current_version: Current plugin version string
        api_url: GitHub API URL to check for releases

    Returns:
        dict: Update information with keys:
            - has_update: bool
            - latest_version: str (if update available)
            - download_url: str (if update available)
            - error: str (if check failed)
    """
    logger.debug("[VERSIONCODE] Starting version check...")
    logger.debug(f"[VERSIONCODE] Current plugin version: {current_version}")
    logger.debug(f"[VERSIONCODE] GitHub API URL: {api_url}")

    try:
        logger.debug("[VERSIONCODE] Sending HTTP request to GitHub API...")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        logger.debug("[VERSIONCODE] GitHub API response received successfully")

        release_data = response.json()
        latest_version = release_data['tag_name'].lstrip('v')  # Remove 'v' prefix
        download_url = release_data['zipball_url']  # Direct zip download

        logger.debug(f"[VERSIONCODE] GitHub release data parsed - Tag: {release_data['tag_name']}")
        logger.debug(f"[VERSIONCODE] Latest version (cleaned): {latest_version}")
        logger.debug(f"[VERSIONCODE] Download URL: {download_url}")

        # Simple string comparison (semver)
        logger.debug(f"[VERSIONCODE] Comparing versions: '{current_version}' vs '{latest_version}'")
        if latest_version > current_version:
            logger.debug(f"[VERSIONCODE] UPDATE AVAILABLE: {current_version} -> {latest_version}")
            logger.debug(f"[VERSIONCODE] Returning update info with download URL")
            return {
                'has_update': True,
                'latest_version': latest_version,
                'download_url': download_url
            }
        else:
            logger.debug(f"[VERSIONCODE] No update available - current version is up to date")
            return {'has_update': False}

    except requests.exceptions.Timeout:
        error_msg = "Update check timed out"
        logger.warning(f"[VERSIONCODE] {error_msg}")
        return {'has_update': False, 'error': error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        logger.warning(f"[VERSIONCODE] {error_msg}")
        return {'has_update': False, 'error': error_msg}

    except Exception as e:
        error_msg = f"Update check failed: {e}"
        logger.warning(f"[VERSIONCODE] {error_msg}")
        return {'has_update': False, 'error': error_msg}
