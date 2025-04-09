"""Constants for the WakaTime integration."""

from datetime import timedelta
import logging

DOMAIN = "wakatime"
LOGGER = logging.getLogger(__package__)

# 600 RPM is rate limit
SCAN_INTERVAL = timedelta(minutes=10)
