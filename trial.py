"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual
from psychopy.core import wait
from time import time, sleep
from response import get_response, check_quit
from stimuli import (
    show_text,
    draw_fixation_dot,
    create_stimulus_frame,
    create_cue_frame,
    create_feedback_frame,
)
from eyetracker import get_trigger
import random


def generate_trial_characteristics(conditions):
    # Extract condition information
    target_item, positions, duration_order = conditions

    # Decide on random durations of stimuli
    duration_dict = {"short": random.randint(200, 800), "long": random.randint(1200, 1800)}
    durations = (duration_dict[duration_order[0]], duration_dict[duration_order[1]])

    return {
        "ITI": random.randint(500, 800),
        "target_item": target_item,
        "target_position": positions[0] if target_item == 1 else positions[1],
        "target_duration": durations[0] if target_item == 1 else durations[1],
        "target_duration_cat": duration_order[0] if target_item == 1 else duration_order[1],
        "positions": positions,
        "durations": durations,
    }


def do_while_showing(waiting_time, something_to_do, window):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    window.flip()
    start = time()
    something_to_do()
    wait(waiting_time - (time() - start))


def single_trial(
    ITI,
    target_item,
    target_position,
    target_duration,
    target_duration_cat,
    positions,
    durations,
    settings,
    testing,
    eyetracker=None,
):
    # Initial fixation cross to eliminate jitter caused by for loop
    draw_fixation_dot(settings)

    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (ITI / 1000, lambda: draw_fixation_dot(settings), None),
        (
            durations[0] / 1000,
            lambda: create_stimulus_frame(positions[0], 1, settings),
            "stimulus_onset_1",
        ),
        (0.75, lambda: draw_fixation_dot(settings), None),
        (
            durations[1] / 1000,
            lambda: create_stimulus_frame(positions[1], 2, settings),
            "stimulus_onset_2",
        ),
        (0.75, lambda: draw_fixation_dot(settings), None),
        (0.25, lambda: create_cue_frame(target_item, settings), "cue_onset"),
        (1.00, lambda: draw_fixation_dot(settings), None),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen. !!!
    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, positions, target_item)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Check for pressed 'q'
        check_quit(settings["keyboard"])

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

    # The for loop only draws the last frame, never shows it
    # So show it here
    settings["window"].flip()
    wait(screens[-1][0])

    response = get_response(
        target_duration,
        positions,
        target_item,
        settings,
        testing,
        eyetracker,
    )

    # Show performance (and feedback on premature key usage if necessary)
    create_feedback_frame(target_duration, response["response_time_in_ms"], response["performance"], settings)

    if response["premature_pressed"] == True:
        show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

    if not testing:
        trigger = get_trigger("feedback_onset", positions, target_item)
        eyetracker.tracker.send_message(f"trig{trigger}")

    settings["window"].flip()
    sleep(0.35)

    return {
        "condition_code": get_trigger("stimulus_onset_1", positions, target_item),
        **response,
    }
