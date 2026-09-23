"""ImageNet visual adapter for ECHO Homework.

The adapter is intentionally reference-based: it does not download, archive,
or redistribute ImageNet image bytes. An authorized caller supplies synset to
image-reference mappings. Lobby permission is checked before references can
be viewed.
"""

from hashlib import sha256


class ImageNetAdapter:
    source_name = "ImageNet"

    def __init__(self, governor, synset_images=None):
        self.governor = governor
        self.synset_images = {
            key: list(value) for key, value in (synset_images or {}).items()
        }
        self.exposure_log = []

    def add_synset(self, synset, image_refs):
        """Register authorized external references; no image bytes are stored."""
        self.synset_images[synset] = list(image_refs)

    def examples(self, word, synset, limit=5):
        """Return temporary references only for an instantiated Lobby word."""
        word = self.governor.require_lobby(word)
        if not synset:
            raise ValueError("A WordNet synset is required for ImageNet lookup")
        refs = list(self.synset_images.get(synset, ()))[: max(0, int(limit))]
        self.exposure_log.append({
            "word": word,
            "synset": synset,
            "source": self.source_name,
            "count": len(refs),
            "reference_hashes": [
                sha256(str(ref).encode("utf-8")).hexdigest() for ref in refs
            ],
        })
        return refs

    def audit(self):
        """Audit visual exposure without reproducing third-party image references."""
        return list(self.exposure_log)
