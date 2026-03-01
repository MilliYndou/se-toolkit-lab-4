"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_returns_empty_when_no_match() -> None:
    """Test that filter returns empty list when no interactions match the item_id."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2), _make_log(3, 3, 3)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_returns_multiple_matches() -> None:
    """Test that filter returns all interactions with the same item_id."""
    interactions = [
        _make_log(1, 1, 1), 
        _make_log(2, 2, 2),
        _make_log(3, 1, 1),  # Same item_id as first
        _make_log(4, 3, 1)   # Same item_id as first
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(log.item_id == 1 for log in result)
    assert {log.id for log in result} == {1, 3, 4}
