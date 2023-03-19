"""."""

# Experimenting with the pyglet library
import pyglet
from pyglet.window import key
from enum import Enum
from pyglet.shapes import Rectangle
from dataclasses import dataclass


@dataclass
class Velocity:
    """."""

    x: int
    y: int


class Paddle(pyglet.shapes.Rectangle):
    """."""

    paddle_velocity = 6

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        # self.velocity = Velocity(0, 0)
        self.movedir = 0

    def top_y(self):
        """."""
        return self.y + self.height // 2

    def bot_y(self):
        """."""
        return self.y - self.height // 2

    def move_up(self, toggle):
        """."""
        self.movedir = 1 if toggle else 0

    def move_down(self, toggle):
        """."""
        self.movedir = -1 if toggle else 0

    def move(self):
        """."""
        self.y += self.movedir * self.paddle_velocity


class Pong(pyglet.window.Window):
    """."""

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)

        self.paddle_height = 150
        self.paddle_width = 25

        Paddle._anchor_x = self.paddle_width // 2
        Paddle._anchor_y = self.paddle_height // 2

        self.player1_paddle = Paddle(
            x=50,
            y=self.height // 2,
            height=self.paddle_height,
            width=self.paddle_width
        )

        self.player2_paddle = Paddle(
            x=self.width - 50,
            y=self.height // 2,
            height=self.paddle_height,
            width=self.paddle_width
        )

    def on_key_press(self, symbol, modifiers):
        """."""
        up_events = [key.W, key.UP]
        # down_events = [key.S, key.DOWN]

        p1_events = [key.W, key.S]
        p2_events = [key.UP, key.DOWN]

        if symbol in p1_events:
            if symbol in up_events:
                self.player1_paddle.move_up(True)
            else:
                self.player1_paddle.move_down(True)
        if symbol in p2_events:
            if symbol in up_events:
                self.player2_paddle.move_up(True)
            else:
                self.player2_paddle.move_down(True)

        if symbol == key.Q:
            print("Pressed: Q")
            print("ENDING GAME")
            raise Exception("QUIT GAME")

    def on_key_release(self, symbol, modifiers):
        """."""
        up_events = [key.W, key.UP]
        # down_events = [key.S, key.DOWN]

        p1_events = [key.W, key.S]
        p2_events = [key.UP, key.DOWN]

        if symbol in p1_events:
            if symbol in up_events:
                self.player1_paddle.move_up(False)
            else:
                self.player1_paddle.move_down(False)
        if symbol in p2_events:
            if symbol in up_events:
                self.player2_paddle.move_up(False)
            else:
                self.player2_paddle.move_down(False)

    def draw_paddles(self, p1: Paddle, p2: Paddle):
        """."""
        if p1.top_y() <= self.height and p1.bot_y() >= 0:
            p1.move()
        if p2.top_y() <= self.height and p2.bot_y() >= 0:
            p2.move()
        p1.draw()
        p2.draw()

    def on_draw(self):
        """."""
        self.clear()

        self.draw_paddles(self.player1_paddle,
                          self.player2_paddle)


pong = Pong(800, 600)
pyglet.app.run()
