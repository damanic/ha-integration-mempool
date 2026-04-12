![Mempool logo](https://raw.githubusercontent.com/damanic/ha-integration-mempool/refs/heads/master/custom_components/mempool/brand/logo.png)

# Mempool.space integration for Home Assistant

A Home Assistant custom integration that exposes Bitcoin network metrics from [mempool.space](https://mempool.space) as sensors. Works with both the public API and self-hosted instances.

### Key Features
- 🚀 **Recommended Fees**: Real-time fee estimates (Fastest, Half Hour, Economy).
- ⛓️ **Blockchain Stats**: Monitor block height and difficulty adjustments.
- ⛏️ **Mining Insights**: Track network hashrate and miner rewards.
- 💰 **BTC Price**: Real-time Bitcoin price in multiple currencies.

---

### Sensors
All sensors appear under a single **Mempool** device.

**Recommended Fees** 
- **Fastest Fee**: Next-block fee estimate (sat/vB)
- **Half Hour Fee**: ~30 min confirmation target (sat/vB)
- **Hour Fee**: ~60 min confirmation target (sat/vB)
- **Economy Fee**: Low-priority fee estimate (sat/vB)
- **Minimum Fee**: Minimum relay fee (sat/vB)

**Blockchain & Mempool**
- **Block Height**: Current blockchain tip height
- **Mempool TX Count**: Unconfirmed transaction count
- **Mempool Size**: Mempool virtual size (vB)
- **Network Hashrate**: Current network hashrate (EH/s)
- **Network Difficulty**: Current mining difficulty

**Difficulty Adjustment** 
- **Progress**: % through current retarget epoch
- **Estimate**: % estimated next adjustment
- **Remaining Blocks**: Blocks until next retarget

**Mining Reward Stats** (Last 144 blocks)
- **Total Miners Reward**: Total revenue (BTC)
- **Avg Block Fees**: Average fees per block (BTC)
- **Avg TX Fee**: Average fee per transaction (sats)

**BTC Price** 
- **USD State**: Current Bitcoin price in USD.
- **Attributes**: EUR, GBP, CAD, etc. Access via templates:
    - `{{ state_attr('sensor.mempool_btc_price', 'eur') }}`



## Example Use Cases

### Mining Break-Even Calculator

You can use the sensors from this integration to calculate the maximum electricity price (per kWh) at which your miner breaks even. This template replaces hardcoded fee estimates, exchange rates, and block subsidy values with live data from the Mempool integration.

See the [Mining Break-Even kWh Price Template](mining-breakeven-template.md) for more details and the full configuration example.


## Installation

### HACS

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
