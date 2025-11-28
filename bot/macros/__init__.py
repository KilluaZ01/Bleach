"""Macro actions for game automation"""

from .basic_actions import tap_macro, swipe_macro, input_macro

from .fight_actions import basic_attack_combo, basic_attack_combo_dodge

from .game_actions import (
    launch_game,
    quit_game,
    open_game,
    open_luck,
)

__all__ = [
    'tap_macro',
    'swipe_macro',
    'input_macro',
    'launch_game',
    'quit_game',
    'open_game',
    'open_luck',
    'basic_attack_combo',
    'basic_attack_combo_dodge',
]