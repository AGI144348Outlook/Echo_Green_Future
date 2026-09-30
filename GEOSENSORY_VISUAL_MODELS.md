# Geosensory visual-model seam

`src/geosensory_model.py` converts a supplied USGS GeoJSON feed into geographic points with coordinates, depth units, event time, magnitude type, source and coverage. It does not fetch, write D1, or claim a live connection. Earthquake locations/magnitudes are catalog-derived estimates, not raw sensor readings. Feed generation freshness is separate from event age. Null values remain missing, zero remains zero, and malformed coordinates are rejected.

Reference: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

Next adapters: coastal observations, solar-wind series, then instrument/station telemetry. Each needs its own measured/derived classification, units, coordinate frame, observation timestamp, freshness threshold, physical instrument provenance and coverage. Endpoint metadata alone must never become a sensed observation. Conceptual diagrams must carry `information_kind: conceptual`.

Validation: `python -m unittest discover -s tests -p test_geosensory_model.py`. Synthetic fixtures are labeled tests; no live values are supplied. Existing migration workflow is unchanged. Production persistence and visualization UI remain separate integration work.
