"""Sensor platform for the Mempool integration."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import MempoolDataUpdateCoordinator
from .data import MempoolConfigEntry
from .entity import MempoolEntity

SENSOR_DATA_MAP: dict[str, Callable[[dict[str, Any]], Any]] = {
    "fastest_fee": lambda data: data["fees"]["fastestFee"],
    "half_hour_fee": lambda data: data["fees"]["halfHourFee"],
    "hour_fee": lambda data: data["fees"]["hourFee"],
    "economy_fee": lambda data: data["fees"]["economyFee"],
    "minimum_fee": lambda data: data["fees"]["minimumFee"],
    "mempool_tx_count": lambda data: data["mempool"]["count"],
    "mempool_size": lambda data: data["mempool"]["vsize"],
    "block_height": lambda data: data["tip_height"],
    "difficulty_progress": lambda data: data["difficulty_adjustment"][
        "progressPercent"
    ],
    "difficulty_change": lambda data: data["difficulty_adjustment"][
        "difficultyChange"
    ],
    "remaining_blocks": lambda data: data["difficulty_adjustment"][
        "remainingBlocks"
    ],
    "network_hashrate": lambda data: round(
        data["hashrate"]["currentHashrate"] / 1e18, 2
    ),
    "network_difficulty": lambda data: data["hashrate"]["currentDifficulty"],
    "total_miners_reward": lambda data: round(
        int(data["reward_stats"]["totalReward"]) / 1e8, 4
    ),
    "avg_block_fees": lambda data: round(
        int(data["reward_stats"]["totalFee"]) / 144 / 1e8, 8
    ),
    "avg_tx_fee": lambda data: round(
        int(data["reward_stats"]["totalFee"])
        / max(int(data["reward_stats"]["totalTx"]), 1),
        0,
    ),
    "latest_block_miner": lambda data: data["latest_block"]["extras"]["pool"]["name"],
    "btc_price": lambda data: data["price"].get("USD"),
}

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="fastest_fee",
        name="Fastest fee",
        icon="mdi:speedometer",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="half_hour_fee",
        name="Half hour fee",
        icon="mdi:speedometer-medium",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="hour_fee",
        name="Hour fee",
        icon="mdi:speedometer-slow",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="economy_fee",
        name="Economy fee",
        icon="mdi:snail",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="minimum_fee",
        name="Minimum fee",
        icon="mdi:arrow-down",
        native_unit_of_measurement="sat/vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="mempool_tx_count",
        name="Mempool TX count",
        icon="mdi:swap-horizontal",
        native_unit_of_measurement="transactions",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="mempool_size",
        name="Mempool size",
        icon="mdi:database",
        native_unit_of_measurement="vB",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="block_height",
        name="Block height",
        icon="mdi:cube-outline",
    ),
    SensorEntityDescription(
        key="difficulty_progress",
        name="Difficulty adjustment progress",
        icon="mdi:percent",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="difficulty_change",
        name="Difficulty adjustment estimate",
        icon="mdi:chart-line",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="remaining_blocks",
        name="Difficulty adjustment remaining blocks",
        icon="mdi:cube-unfolded",
        native_unit_of_measurement="blocks",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="network_hashrate",
        name="Network hashrate",
        icon="mdi:flash",
        native_unit_of_measurement="EH/s",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="network_difficulty",
        name="Network difficulty",
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="total_miners_reward",
        name="Total miners reward (144 blocks)",
        icon="mdi:bitcoin",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=4,
    ),
    SensorEntityDescription(
        key="avg_block_fees",
        name="Avg block fees (144 blocks)",
        icon="mdi:cash-multiple",
        native_unit_of_measurement="BTC",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=8,
    ),
    SensorEntityDescription(
        key="avg_tx_fee",
        name="Avg TX fee (144 blocks)",
        icon="mdi:cash",
        native_unit_of_measurement="sats",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="latest_block_miner",
        name="Latest block miner",
        icon="mdi:pickaxe",
    ),
    SensorEntityDescription(
        key="btc_price",
        name="BTC price",
        icon="mdi:currency-usd",
        native_unit_of_measurement="USD",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MempoolConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Mempool sensors from a config entry."""
    coordinator = entry.runtime_data.coordinator

    entities: list[MempoolSensor] = []
    for description in SENSOR_DESCRIPTIONS:
        if description.key == "btc_price":
            entities.append(MempoolPriceSensor(coordinator, description))
        elif description.key == "latest_block_miner":
            entities.append(MempoolLatestBlockMinerSensor(coordinator, description))
        else:
            entities.append(MempoolSensor(coordinator, description))

    async_add_entities(entities)


class MempoolSensor(MempoolEntity, SensorEntity):
    """Representation of a Mempool sensor."""

    @property
    def native_value(self) -> Any | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        try:
            return SENSOR_DATA_MAP[self.entity_description.key](
                self.coordinator.data
            )
        except (KeyError, TypeError):
            return None


class MempoolLatestBlockMinerSensor(MempoolSensor):
    """Latest block miner sensor with pool attributes."""

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return pool slug and miner names as attributes."""
        if self.coordinator.data is None:
            return None
        try:
            pool = self.coordinator.data["latest_block"]["extras"]["pool"]
            return {
                "slug": pool.get("slug"),
                "miner_names": pool.get("minerNames"),
            }
        except (KeyError, TypeError):
            return None


class MempoolPriceSensor(MempoolSensor):
    """BTC Price sensor with currency attributes."""

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return other currencies as attributes."""
        if self.coordinator.data is None:
            return None
        price = self.coordinator.data.get("price", {})
        return {k.lower(): v for k, v in price.items() if k != "USD"}
