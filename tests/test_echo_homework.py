import pytest

from src.echo_homework import HomeworkGovernor
from src.echo_gf_wordnet import GFWordNetAdapter
from src.echo_imagenet import ImageNetAdapter
from src.echo_live_image_search import LiveImageSearchAdapter
from src.echo_homework_audit import HomeworkAudit


def test_unknown_word_cannot_be_studied():
    governor = HomeworkGovernor(["water"])
    with pytest.raises(PermissionError):
        governor.require_lobby("oxygen")


def test_definition_creates_candidates_not_lobby_members():
    governor = HomeworkGovernor(["water"])
    gf = GFWordNetAdapter(governor)
    gf.add_entry("water", "a clear liquid compound", synset="water.n.01")

    result = gf.study_definition("water")

    assert "liquid" in result["candidates"]
    assert "liquid" in governor.candidates
    assert "liquid" not in governor.lobby


def test_discovered_word_can_be_instantiated_with_lineage():
    governor = HomeworkGovernor(["water"])
    gf = GFWordNetAdapter(governor)
    gf.add_entry("water", "a clear liquid compound")
    gf.study_definition("water")

    admitted = governor.instantiate(["liquid"], parent="water")

    assert admitted == ["liquid"]
    assert governor.lineage["liquid"] == {
        "source": "definition",
        "parent": "water",
    }


def test_imagenet_requires_lobby_permission():
    governor = HomeworkGovernor(["dog"])
    images = ImageNetAdapter(
        governor,
        {"dog.n.01": ["image-a", "image-b"]},
    )

    assert images.examples("dog", "dog.n.01") == ["image-a", "image-b"]

    with pytest.raises(PermissionError):
        images.examples("cat", "cat.n.01")


def test_live_search_is_lobby_gated_and_bounded():
    governor = HomeworkGovernor(["dog"])

    def provider(word, limit):
        return [f"{word}-{i}" for i in range(20)]

    search = LiveImageSearchAdapter(governor, provider, max_results=3)

    assert len(search.search("dog", limit=10)) == 3

    with pytest.raises(PermissionError):
        search.search("cat")


def test_visual_audits_store_hashes_not_references():
    governor = HomeworkGovernor(["dog"])
    secret_reference = "temporary-image-reference"

    images = ImageNetAdapter(
        governor,
        {"dog.n.01": [secret_reference]},
    )
    images.examples("dog", "dog.n.01")

    assert secret_reference not in str(images.audit())


def test_homework_audit_freezes_pre_exam_state():
    governor = HomeworkGovernor(["water"])
    audit = HomeworkAudit()
    audit.record_seed("water")
    frozen = audit.freeze(governor.snapshot())

    assert frozen["frozen"] is True
    assert frozen["audit_sha256"]

    with pytest.raises(RuntimeError):
        audit.record_seed("dog")
