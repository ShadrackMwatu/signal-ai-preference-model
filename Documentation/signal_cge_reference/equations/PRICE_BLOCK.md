# Price Block

The price block links producer prices, consumer prices, import prices, export prices, taxes, margins, and the numeraire.

Placeholder structure:

```text
consumer_price(c) = producer_price(c) + taxes(c) + margins(c)
import_price(c) = world_import_price(c) * exchange_rate * (1 + tariff_rate(c))
```

The numeraire closure must identify one reference price or index to anchor relative prices.
