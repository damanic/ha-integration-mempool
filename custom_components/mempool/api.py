"""API client for mempool.space."""

from __future__ import annotations

from typing import Any

import aiohttp


class MempoolApiError(Exception):
    """Base exception for Mempool API errors."""


class MempoolApiConnectionError(MempoolApiError):
    """Exception for connection errors."""


class MempoolApiClient:
    """Async API client for mempool.space."""

    def __init__(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._base_url = base_url.rstrip("/")
        self._session = session

    async def _get(self, path: str) -> Any:
        """Make a GET request and return parsed response."""
        url = f"{self._base_url}{path}"
        try:
            async with self._session.get(url) as resp:
                resp.raise_for_status()
                content_type = resp.content_type
                if content_type == "text/plain":
                    return await resp.text()
                return await resp.json()
        except (aiohttp.ClientConnectionError, TimeoutError) as err:
            raise MempoolApiConnectionError(
                f"Error connecting to {url}"
            ) from err
        except aiohttp.ClientResponseError as err:
            raise MempoolApiError(
                f"Error response {err.status} from {url}"
            ) from err
        except Exception as err:
            raise MempoolApiError(
                f"Unexpected error fetching {url}"
            ) from err

    async def async_get_backend_info(self) -> dict[str, Any]:
        """Get backend info (used for connection validation)."""
        return await self._get("/api/v1/backend-info")

    async def async_get_fees_recommended(self) -> dict[str, Any]:
        """Get recommended fees."""
        return await self._get("/api/v1/fees/recommended")

    async def async_get_mempool(self) -> dict[str, Any]:
        """Get mempool statistics."""
        return await self._get("/api/mempool")

    async def async_get_tip_height(self) -> int:
        """Get current block tip height."""
        return int(await self._get("/api/blocks/tip/height"))

    async def async_get_tip_hash(self) -> str:
        """Get current block tip hash."""
        return await self._get("/api/blocks/tip/hash")

    async def async_get_block(self, block_hash: str) -> dict[str, Any]:
        """Get block details by hash."""
        return await self._get(f"/api/v1/block/{block_hash}")

    async def async_get_difficulty_adjustment(self) -> dict[str, Any]:
        """Get difficulty adjustment information."""
        return await self._get("/api/v1/difficulty-adjustment")

    async def async_get_hashrate(self) -> dict[str, Any]:
        """Get mining hashrate data."""
        return await self._get("/api/v1/mining/hashrate/1m")

    async def async_get_reward_stats(self) -> dict[str, Any]:
        """Get mining reward stats for the last 144 blocks."""
        return await self._get("/api/v1/mining/reward-stats/144")

    async def async_get_prices(self) -> dict[str, Any]:
        """Get current prices."""
        return await self._get("/api/v1/prices")
