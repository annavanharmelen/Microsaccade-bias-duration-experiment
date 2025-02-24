"""
This file contains the functions necessary for
creating the interactive response dial at the end of a trial.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import event
from psychopy.hardware.keyboard import Keyboard
from time import time
from eyetracker import get_trigger
from stimuli import draw_one_stimulus, draw_fixation_dot


def evaluate_response(target_duration, response_duration):
    duration_diff = response_duration - target_duration
    duration_diff_abs = abs(duration_diff)
    performance = round(duration_diff)
    sign = "+" if duration_diff > 0 else ""
    return {
        "duration_offset": round(duration_diff),
        "duration_diff_abs": round(duration_diff_abs),
        "performance": f"{sign}{performance}",
    }


def get_response(
    target_duration,
    positions,
    target_item,
    settings,
    testing,
    eyetracker,
):
    keyboard: Keyboard = settings["keyboard"]

    # Check for pressed 'q'
    check_quit(keyboard)

    # Show response can start
    draw_fixation_dot(settings, [-1, -1, -1])
    settings["window"].flip()

    # These timing systems should start at the same time, this is almost true
    idle_reaction_time_start = time()
    keyboard.clock.reset()

    # Check if _any_ keys were prematurely pressed
    prematurely_pressed = [(p.name, p.rt) for p in keyboard.getKeys()]
    keyboard.clearEvents()

    # Wait for space key press
    keyboard.clock.reset()
    key = keyboard.waitKeys(keyList=["space"], waitRelease=False)
    response_started = time()

    if not testing and eyetracker:
        trigger = get_trigger("response_onset", positions, target_item)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Show target item while space is held
    while keyboard.getState("space"):
        draw_one_stimulus("middle", settings)
        settings["window"].flip()

    # Compute both reaction times
    response_time = time() - response_started
    idle_reaction_time = response_started - idle_reaction_time_start

    if not testing and eyetracker:
        trigger = get_trigger("response_offset", positions, target_item)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Make sure keystrokes made during this trial don't influence the next
    keyboard.clearEvents()

    return {
        "idle_reaction_time_in_ms": round(idle_reaction_time * 1000, 2),
        "response_time_in_ms": round(response_time * 1000, 2),
        "key_pressed": key[0].name,
        "premature_pressed": True if prematurely_pressed else False,
        "premature_key": prematurely_pressed[0][0] if prematurely_pressed else None,
        "premature_timing": (
            round(prematurely_pressed[0][1] * 1000, 2) if prematurely_pressed else None
        ),
        **evaluate_response(target_duration, response_time * 1000),
    }


def wait_for_key(key_list, keyboard):
    keyboard: Keyboard = keyboard
    keyboard.clearEvents()
    keys = keyboard.waitKeys(keyList=key_list)

    return keys


def check_quit(keyboard):
    if keyboard.getKeys("q"):
        raise KeyboardInterrupt()
