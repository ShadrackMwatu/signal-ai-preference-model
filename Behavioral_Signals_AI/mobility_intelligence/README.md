# Mobility and Place Activity Intelligence

This module adds privacy-preserving place intelligence to Behavioral Signals AI.

It does **not** perform surveillance. It does **not** track individuals. It does **not** store routes, device identifiers, home locations, work locations, private movement histories, or raw footfall trails.

The module learns only from aggregated place intelligence and legally accessible public Google Maps ecosystem signals, such as public place metadata, categories, ratings, review counts, opening hours, business status, place prominence, and other public relevance indicators where available.

## Philosophy

People reveal priorities through aggregated place interaction patterns and public economic activity signals. Signal uses those aggregate patterns to infer category-level demand, infrastructure pressure, preference signals, and opportunity zones without identifying or tracking people.

## What It Processes

- Public place metadata
- Place categories
- Ratings and review counts
- Opening hours and business status
- Aggregated category prominence
- Public place relevance indicators

## What It Never Processes

- User IDs
- Device IDs
- IMEI numbers
- Phone numbers
- GPS traces
- Routes
- Home or work locations
- Individual coordinates
- Personal movement histories

## How It Supports Behavioral Signals AI

1. Optional Google Maps ecosystem connector reads public place metadata when `GOOGLE_MAPS_API_KEY` is configured.
2. The privacy guard rejects person-level mobility fields.
3. Place records are classified into economic demand categories.
4. Popularity and place relevance are converted into aggregated demand signals.
5. Signals reinforce or re-rank the existing Live Signal Feed when they match current demand categories.

## Configuration

Safe defaults:

```text
ENABLE_MOBILITY_INTELLIGENCE=true
MOBILITY_SOURCE_MODE=google_maps_ecosystem
ALLOW_PERSONAL_LOCATION_DATA=false
GOOGLE_MAPS_API_KEY=<optional secret>
```

If no Google Maps key is available, the app continues to run and uses cached aggregate place intelligence if available.