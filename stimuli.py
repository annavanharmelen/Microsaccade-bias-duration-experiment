"""
This file contains the functions necessary for
creating the fixation cross and the bar stimuli.
To run the 'microsaccade bias duration' experiment, see main.py.

made by Anna van Harmelen, 2025
"""

from psychopy import visual

DOT_SIZE = 0.1  # diameter of circle
ECCENTRICITY = 6
ITEM_SIZE = 1


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=22
    )

    textstim.draw()


def draw_fixation_dot(settings, colour="#eaeaea"):
    # Make fixation dot
    fixation_dot = visual.Circle(
        win=settings["window"],
        units="pix",
        radius=settings["deg2pix"](DOT_SIZE),
        pos=(0, 0),
        fillColor=colour,
    )

    fixation_dot.draw()


def draw_one_stimulus(position, settings, order=0):
    # Check input
    if position == "left":
        pos = (-settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "right":
        pos = (settings["deg2pix"](ECCENTRICITY), 0)
    elif position == "middle":
        pos = (0, 0)
        colour = [1, 1, 1]
    else:
        raise Exception(f"Expected position 'left' or 'right', but received {position!r}.")
    
    if position != "middle":
        if order == 1:
            colour = [(rgb_value / 128 - 1) for rgb_value in [238, 104, 60]]
        elif order == 2:
            colour = [(rgb_value / 128 - 1) for rgb_value in [101, 148, 14]]
        else:
            raise Exception(f"Expected order 1 or 2, but received {order!r}.")

    item = visual.Rect(
        win=settings["window"],
        units="pix",
        width=settings["deg2pix"](ITEM_SIZE),
        height=settings["deg2pix"](ITEM_SIZE),
        pos=pos,
        fillColor=colour,
        #fillColor=[1, 1, 1],
    )

    item.draw()


def create_stimulus_frame(item_position, item_order, settings):
    draw_fixation_dot(settings)
    draw_one_stimulus(item_position, settings, item_order)


def create_cue_frame(target_item, settings):
    draw_fixation_dot(settings)
    show_text(target_item, settings["window"], pos=(0, settings["deg2pix"](0.3)))


def create_feedback_frame(target_duration, response_duration, main_feedback, settings):
    draw_fixation_dot(settings)
    show_text(
        f"{main_feedback}",
        settings["window"],
        (0, settings["deg2pix"](0.3)),
    )
