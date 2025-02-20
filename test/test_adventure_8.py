import pytest
from adventure import enter_dungeon, find_clue
from unittest.mock import patch
import io
import sys

def test_cryptic_library_room_clues_found(capsys):
    dungeon_rooms = [("The Cryptic Library", None, "library", None)]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}

    enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
    captured = capsys.readouterr()
    assert "You enter the Cryptic Library." in captured.out
    assert "You discovered a new clue:" in captured.out
    assert len(clues) >= 1 # At least one clue should be found

def test_cryptic_library_room_staff_of_wisdom_effect(capsys):
    dungeon_rooms = [("The Cryptic Library", None, "library", None)]
    player_stats = {'health': 100, 'attack': 5}
    inventory = ["staff_of_wisdom"] # Player has the staff
    clues = set()
    artifacts = {}

    enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
    captured = capsys.readouterr()
    assert "The Staff of Wisdom hums in your hand" in captured.out
    assert "You feel you could now bypass a puzzle" in captured.out

def test_cryptic_library_room_no_staff_no_bypass_message(capsys):
    dungeon_rooms = [("The Cryptic Library", None, "library", None)]
    player_stats = {'health': 100, 'attack': 5}
    inventory = [] # Player does not have staff
    clues = set()
    artifacts = {}

    enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
    captured = capsys.readouterr()
    assert "The Staff of Wisdom hums in your hand" not in captured.out
    assert "You feel you could now bypass a puzzle" not in captured.out # No bypass message

def test_cryptic_library_room_finds_two_clues():
    dungeon_rooms = [("The Cryptic Library", None, "library", None)]
    player_stats = {'health': 100, 'attack': 5}
    inventory = []
    clues = set()
    artifacts = {}

    enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts)
    assert len(clues) == 2 # Exactly two clues should be found (as per assignment spec)
