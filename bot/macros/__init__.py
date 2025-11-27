"""Macro actions for game automation"""

from .basic_actions import tap_macro, swipe_macro, input_macro
from .game_actions import (
    launch_game,
    quit_game,
    open_game,
    open_luck,
    tap_if_regular_summon,
)

__all__ = [
    'tap_macro',
    'swipe_macro',
    'input_macro',
    'launch_game',
    'quit_game',
    'open_game',
    'open_luck',
    'tap_if_regular_summon',
]