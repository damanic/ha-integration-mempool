"""DataUpdateCoordinator for the Mempool integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MempoolApiClient, MempoolApiError
from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN, LOGGER


class MempoolDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to poll mempool.space API endpoints."""

    def __init__(self, hass: HomeAssistant, client: MempoolApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from all endpoints concurrently."""
        try:
            results = await asyncio.gather(
                self.client.async_get_fees_recommended(),
                self.client.async_get_mempool(),
                self.client.async_get_tip_hash(),
                self.client.async_get_difficulty_adjustment(),
                self.client.async_get_hashrate(),
                self.client.async_get_reward_stats(),
                self.client.async_get_prices(),
            )
        except MempoolApiError as err:
            raise UpdateFailed(f"Error fetching mempool data: {err}") from err

        (
            fees, mempool, tip_hash, difficulty,
            hashrate, reward_stats, price_data,
        ) = results

        # Fetch latest block using tip hash
        try:
            latest_block = await self.client.async_get_block(tip_hash)
        except MempoolApiError as err:
            raise UpdateFailed(f"Error fetching latest block: {err}") from err

        # /api/v1/prices returns flat {time, USD, EUR, ...} — strip the time key
        price = {k: v for k, v in price_data.items() if k != "time"}

        return {
            "fees": fees,
            "mempool": mempool,
            "tip_height": latest_block["height"],
            "difficulty_adjustment": difficulty,
            "hashrate": hashrate,
            "reward_stats": reward_stats,
            "latest_block": latest_block,
            "price": price,
        }
