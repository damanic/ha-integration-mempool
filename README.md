<p align="center">
  <img src="custom_components/mempool/logo.png" alt="Mempool logo" width="128">
</p>

# Mempool.space integration for Home Assistant

A Home Assistant custom integration that exposes Bitcoin network metrics from [mempool.space](https://mempool.space) as sensors. Works with both the public API and self-hosted instances.

## Sensors

All sensors appear under a single **Mempool** device, grouped by the API endpoint they source data from.

### Recommended Fees
`GET /api/v1/fees/recommended`

| Sensor | Unit | Description |
|--------|------|-------------|
| Fastest Fee | sat/vB | Next-block fee estimate |
| Half Hour Fee | sat/vB | ~30 minute confirmation target |
| Hour Fee | sat/vB | ~60 minute confirmation target |
| Economy Fee | sat/vB | Low-priority fee estimate |
| Minimum Fee | sat/vB | Minimum relay fee |

### Mempool
`GET /api/mempool`

| Sensor | Unit | Description |
|--------|------|-------------|
| Mempool TX Count | transactions | Unconfirmed transaction count |
| Mempool Size | vB | Mempool virtual size |

### Block Height
`GET /api/blocks/tip/height`

| Sensor | Unit | Description |
|--------|------|-------------|
| Block Height | — | Current blockchain tip height |

### Difficulty Adjustment
`GET /api/v1/difficulty-adjustment`

| Sensor | Unit | Description |
|--------|------|-------------|
| Difficulty Adjustment Progress | % | Progress through current retarget epoch |
| Difficulty Adjustment Estimate | % | Estimated next difficulty adjustment |
| Difficulty Adjustment Remaining Blocks | blocks | Blocks until next retarget |

### Mining Hashrate
`GET /api/v1/mining/hashrate/1m`

| Sensor | Unit | Description |
|--------|------|-------------|
| Network Hashrate | EH/s | Current network hashrate |
| Network Difficulty | — | Current mining difficulty |

### Mining Reward Stats
`GET /api/v1/mining/reward-stats/144`

| Sensor | Unit | Description |
|--------|------|-------------|
| Total Miners Reward (144 blocks) | BTC | Total miner revenue over the last 144 blocks |
| Avg Block Fees (144 blocks) | BTC | Average fees per block over the last 144 blocks |
| Avg TX Fee (144 blocks) | sats | Average fee per transaction over the last 144 blocks |

### Latest Block
`GET /api/blocks/tip/hash` + `GET /api/v1/block/{hash}`

| Sensor | Unit | Description |
|--------|------|-------------|
| Latest Block Miner | — | Mining pool that found the latest block (slug and miner names as attributes) |

### Price
`GET /api/v1/prices`

| Sensor | Unit | Description |
|--------|------|-------------|
| BTC Price | USD | Bitcoin price with other currencies as attributes |

The BTC Price sensor stores USD as its state and exposes all other currencies (EUR, GBP, CAD, etc.) as entity attributes. Access them via templates:

```yaml
{{ state_attr('sensor.mempool_btc_price', 'eur') }}
```

## Installation

### HACS (not yet published)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** → **Custom repositories**.
3. Add this repository URL and select **Integration** as the category.
4. Search for **Mempool** and install it.
5. Restart Home Assistant.

### Manual

1. Copy the `custom_components/mempool` folder into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.

## Setup

1. Go to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for **Mempool**.
3. Enter your instance URL (leave the default `https://mempool.space` for the public API, or enter your self-hosted URL).
4. Click **Submit**.

## Rate Limits

The public mempool.space API enforces rate limits, though exact thresholds are [intentionally undisclosed](https://github.com/mempool/mempool/discussions/752). Exceeding limits returns HTTP 429 responses, and repeated violations may result in a ban.

This integration makes **8 API calls per polling cycle** (default: every 5 minutes), which is conservative usage. If you experience 429 errors, consider:

- **Self-hosting** a [mempool instance](https://github.com/mempool/mempool) — self-hosted instances have no rate limits.
- **Mempool Enterprise** at [mempool.space/enterprise](https://mempool.space/enterprise) for higher limits.

No authentication is required for public API access.

## License

MIT
