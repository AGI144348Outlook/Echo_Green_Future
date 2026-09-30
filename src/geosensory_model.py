"""Observation-to-visual-model seam. No network access or persistence side effects."""
from datetime import datetime, timezone
import math

def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def usgs_model(payload, source_url, now_ms, stale_after_ms=900000):
    """USGS event estimates retain provenance; feed freshness is separate from event age."""
    if payload.get('type') != 'FeatureCollection':
        raise ValueError('Expected a GeoJSON FeatureCollection')
    generated = payload.get('metadata', {}).get('generated')
    age = now_ms - generated if finite(generated) else None
    freshness = 'missing' if age is None else ('future' if age < 0 else ('stale' if age > stale_after_ms else 'fresh'))
    points, rejected = [], []
    for feature in payload.get('features', []):
        props = feature.get('properties') or {}
        geometry = feature.get('geometry') or {}
        coords = geometry.get('coordinates') or []
        if geometry.get('type') != 'Point' or len(coords) < 3 or not all(finite(x) for x in coords[:3]) or not -180 <= coords[0] <= 180 or not -90 <= coords[1] <= 90:
            rejected.append({'id': feature.get('id'), 'reason':'missing or invalid coordinates'})
            continue
        magnitude, timestamp = props.get('mag'), props.get('time')
        points.append({
            'id':feature.get('id'), 'coordinates':{'longitude':coords[0], 'latitude':coords[1], 'depth':coords[2], 'depth_unit':'km', 'angular_unit':'degree'},
            'value':magnitude if finite(magnitude) else None, 'quantity':'magnitude', 'unit':props.get('magType'),
            'observed_at_ms':timestamp if finite(timestamp) else None,
            'information_kind':'derived', 'value_status':'available' if finite(magnitude) else 'missing',
            'source':{'feed_url':source_url, 'event_url':props.get('url'), 'event_id':feature.get('id')},
            'lineage':['Earth','seismic event catalog',feature.get('id')],
            'label':props.get('place'), 'review_status':props.get('status'),
        })
    return {'schema_version':1, 'view':'geographic-points', 'generated_at_ms':generated,
            'freshness':freshness, 'feed_age_ms':age, 'coverage':{'description':'Only events selected by the supplied feed; absence is not absence of earthquakes','bounds':payload.get('bbox')},
            'points':points,'rejected':rejected,'source_url':source_url,'persistence':'none'}
