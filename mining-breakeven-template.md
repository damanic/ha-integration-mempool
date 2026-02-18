# Mining Break-Even kWh Price Template

This template sensor calculates the maximum electricity price (AUD per kWh) at which your miner breaks even. It replaces hardcoded fee estimates, exchange rates, and block subsidy values with live data from the Mempool integration.

## Template Sensor

Add this to your `configuration.yaml` under `template:` → `sensor:`:

```yaml
template:
  - sensor:
      - name: "Mining Break-Even kWh Price"
        unit_of_measurement: "AUD/kWh"
        icon: mdi:flash-alert
        state: >
          {% set miner_watts = 3500.0 %}
          {% set miner_ths = 272.0 %}
          {% set pool_fee = 0.02 %}
          {% set blocks_per_day = 144.0 %}

          {% set block_height = states('sensor.mempool_block_height') | int(0) %}
          {% set halvings = (block_height // 210000) %}
          {% set subsidy_btc = 50.0 / (2 ** halvings) %}

          {% set aud_per_btc = state_attr('sensor.mempool_btc_price', 'aud') | float(0) %}
          {% set net_ehs = states('sensor.mempool_network_hashrate') | float(0) %}
          {% set fee_btc = states('sensor.mempool_avg_block_fees') | float(0) %}

          {% set btc_per_block = subsidy_btc + fee_btc %}
          {% set net_hs = net_ehs * 1e18 %}

          {% if aud_per_btc > 0 and net_hs > 0 %}
            {% set miner_hs = miner_ths * 1e12 %}
            {% set share = miner_hs / net_hs %}
            {% set btc_per_day = blocks_per_day * share * btc_per_block * (1.0 - pool_fee) %}
            {% set aud_per_day = btc_per_day * aud_per_btc %}
            {% set kwh_per_day = (miner_watts / 1000.0) * 24.0 %}
            {% set breakeven_raw = aud_per_day / kwh_per_day %}
            {{ ((breakeven_raw * 100) | round(0, 'ceil')) / 100 }}
          {% else %}
            {{ 0 }}
          {% endif %}
```

## Customisation

Update these three variables to match your setup:

| Variable | Description | Example     |
|----------|-------------|-------------|
| `miner_watts` | Miner wall power draw in watts | `3500.0`    |
| `miner_ths` | Miner hashrate in TH/s | `270.0`     |
| `pool_fee` | Mining pool fee as a decimal | `0.02` (2%) |
