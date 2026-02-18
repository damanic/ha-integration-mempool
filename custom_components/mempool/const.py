"""Constants for the Mempool integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "mempool"
ATTRIBUTION = "Data provided by mempool.space"

DEFAULT_BASE_URL = "https://mempool.space"
CONF_BASE_URL = "base_url"
DEFAULT_UPDATE_INTERVAL = 300  # seconds
