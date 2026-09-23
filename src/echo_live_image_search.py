"""Controlled live-image search adapter for ECHO Homework.

This is a provider boundary, not a scraper. A caller supplies an authorized
image-search function. Only Lobby-instantiated words may be searched.
Returned references are ephemeral; the audit retains hashes, not image bytes
or URLs.
"""

from hashlib import sha256


class LiveImageSearchAdapter:
    source_name = "Live Image Search"

    def __init__(self, governor, search_provider, max_results=8):
        if not callable(search_provider):
            raise TypeError("search_provider must be callable")
        self.governor = governor
        self.search_provider = search_provider
        self.max_results = max(1, int(max_results))
        self.exposure_log = []

    def search(self, word, limit=5):
        word = self.governor.require_lobby(word)
        limit = min(max(1, int(limit)), self.max_results)

        results = list(self.search_provider(word, limit=limit))[:limit]

        self.exposure_log.append({
            "word": word,
            "source": self.source_name,
            "count": len(results),
            "reference_hashes": [
                sha256(str(item).encode("utf-8")).hexdigest()
                for item in results
            ],
        })

        # References exist only in the active study call. The adapter itself
        # deliberately retains no URLs or image content.
        return results

    def audit(self):
        return list(self.exposure_log)
