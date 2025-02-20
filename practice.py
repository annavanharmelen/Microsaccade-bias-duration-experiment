"""
This file contains the functions necessary for
practising the trials and the use of the report dial.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

import random
from trial import generate_trial_characteristics
from stimuli import create_stimulus_frame, draw_fixation_dot, show_text
from psychopy.core import wait
from response import get_response, check_quit, wait_for_key
from time import sleep
from trial import single_trial


def practice(eyetracker, settings):
    # Practice response wheel
    practice_response(eyetracker, settings)

    # Practice full trials
    practice_trials(eyetracker, settings)


def practice_response(eyetracker, settings):
    # Practice response until participant chooses to stop
    try:
        # Show first screen
        show_text(
            "Welcome! "
            "Press SPACE to start practicing how to reproduce durations."
            "\n\nRemember to press Q to stop practising.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()
        
        while True:
            # Show fixation dot in preparation
            draw_fixation_dot(settings)
            settings["window"].flip()
            sleep(0.5)

            # Show central square with certain duration
            stimulus = generate_trial_characteristics([1, "left", "right"])
            create_stimulus_frame("middle", settings)
            settings["window"].flip()
            wait(stimulus["target_duration"] / 1000)

            # Delay
            draw_fixation_dot(settings)
            settings["window"].flip()
            wait(1.5)

            # Allow response
            response = get_response(
                stimulus["target_duration"], None, None, settings, True, None
            )
            draw_fixation_dot(settings)
            show_text(
                f"{response['performance']}",
                settings["window"],
                (0, settings["deg2pix"](0.3)),
            )

            if response["premature_pressed"] == True:
                show_text("!", settings["window"], (0, -settings["deg2pix"](0.3)))

            settings["window"].flip()
            sleep(0.25)

            # Pause before next one
            draw_fixation_dot(settings)
            settings["window"].flip()
            sleep(random.randint(1500, 2000) / 1000)

            # Check for pressed 'q'
            check_quit(settings["keyboard"])

    except KeyboardInterrupt:
        show_text(
            "You decided to stop practising the basic response. "
            "Press SPACE to start practicing full trials."
            "\n\nRemember to press Q to stop practising these trials and move on to the final practice part.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()



def practice_trials(eyetracker, settings):
    # Practice full trials until participant chooses to stop
    try:
        while True:
            target_item = random.choice([1, 2])
            loc_1 = random.choice(["left", "right"])
            loc_2 = "right" if loc_1 == "left" else "left"

            trial_characteristics = generate_trial_characteristics(
                (target_item, loc_1, loc_2)
            )

            # Generate trial
            single_trial(
                **trial_characteristics,
                settings=settings,
                testing=True,
                eyetracker=None,
            )

    except KeyboardInterrupt:
        settings["window"].flip()
        show_text(
            "You decided to stop practicing the trials."
            f"\n\nPress SPACE to start the experiment.",
            settings["window"],
        )
        settings["window"].flip()
        if eyetracker:
            keys = wait_for_key(["space", "c"], settings["keyboard"])
            if "c" in keys:
                eyetracker.calibrate()
                eyetracker.start()
                return True
        else:
            wait_for_key(["space"], settings["keyboard"])

        # Make sure the keystroke from starting the experiment isn't saved
        settings["keyboard"].clearEvents()
