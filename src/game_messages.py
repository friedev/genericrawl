import libtcodpy as libtcod

import textwrap


def join_list(terms):
    terms = ', '.join(terms)
    terms = terms.rsplit(',', 1)
    if len(terms) > 2:
        terms = ', and'.join(terms)
    else:
        terms = ' and'.join(terms)
    return terms


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))