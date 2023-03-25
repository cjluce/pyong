"""."""

import pyglet
from pyglet.window import key
from pyglet.math import Vec2
from dataclasses import dataclass


@dataclass
class Velocity:
    """."""

    x: int
    y: int


class PongRect(pyglet.shapes.Rectangle):
    """."""

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        self.anchor_x = self.width // 2
        self.anchor_y = self.height // 2

    def top(self):
        """."""
        return self.y + (self.height // 2)

    def bottom(self):
        """."""
        return self.y - (self.height // 2)

    def right(self):
        """."""
        return self.x + (self.width // 2)

    def left(self):
        """."""
        return self.x - (self.width // 2)


class Paddle(PongRect):
    """."""

    paddle_velocity = 6

    def __init__(self, boundtop, boundbot=0, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        # self.anchor_x = self.width // 2
        # self.anchor_y = self.height // 2
        self.movedir = 0
        self.boundtop = boundtop
        self.boundbot = boundbot

    def top_y(self):
        """."""
        return self.y + self.height // 2

    def bot_y(self):
        """."""
        return self.y - self.height // 2

    def move_up(self):
        """."""
        if self.top_y() <= self.boundtop:
            self.y += self.paddle_velocity

    def move_down(self):
        """."""
        if self.bot_y() >= self.boundbot:
            self.y -= self.paddle_velocity


class Ball(PongRect):
    """."""

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)
        # The initial velocity goes slowly towards player 1. Maybe the
        # ball should switch directions to the previous winner?
        # self.velocity = Velocity(3, 0)
        self.velocity = Vec2(6, 0)

    def move(self):
        """."""
        self.x += self.velocity.x
        self.y += self.velocity.y


class Pong(pyglet.window.Window):
    """."""

    def __init__(self, *args, **kwargs):
        """."""
        super().__init__(*args, **kwargs)

        self.paddle_height = 150
        self.paddle_width = 25

        self.player1_paddle = Paddle(
            boundtop=self.height,
            boundbot=0,
            x=50,
            y=self.height // 2,
            height=self.paddle_height,
            width=self.paddle_width
        )

        self.player2_paddle = Paddle(
            boundtop=self.height,
            boundbot=0,
            x=self.width - 50,
            y=self.height // 2,
            height=self.paddle_height,
            width=self.paddle_width
        )

        self.ball_height = 30
        self.ball_width = 30

        self.ball = Ball(
            x=self.width // 2,
            y=self.height // 2,
            height=self.ball_height,
            width=self.ball_width
        )

        self.linevec = pyglet.shapes.Line(
            x=self.ball.x,
            y=self.ball.y,
            x2=self.ball.x + self.ball.velocity.x,
            y2=self.ball.y + self.ball.velocity.y,
            width=3
        )

        self._paddle_symbol = [key.W, key.S,
                               key.UP, key.DOWN]

        self.pressed = {key.W: False, key.S: False,
                        key.UP: False, key.DOWN: False}
        self.symbolevent = {key.W: self.player1_paddle.move_up,
                            key.S: self.player1_paddle.move_down,
                            key.UP: self.player2_paddle.move_up,
                            key.DOWN: self.player2_paddle.move_down}

    def on_key_press(self, symbol, modifiers):
        """."""
        if symbol in self._paddle_symbol:
            self.pressed[symbol] = True

        if symbol == key.Q:
            print("Pressed: Q")
            print("ENDING GAME")
            raise Exception("QUIT GAME")

    def on_key_release(self, symbol, modifiers):
        """."""
        if symbol in self._paddle_symbol:
            self.pressed[symbol] = False

    def left_side(self, r):
        """Get left side bound of rectangle."""
        return r.x - (r.width // 2)

    def right_side(self, r):
        """Get right side bound of rectangle."""
        return r.x + (r.width // 2)

    def collide_goal(self):
        """."""
        return (self.ball.left() <= 0 or
                self.ball.right() >= self.width)

    def collide_table(self):
        """."""
        return (self.ball.bottom() <= 0 or
                self.ball.top() >= self.height)

    def collide_paddle(self, paddle):
        """."""
        return (paddle.right() >= self.ball.left() and
                paddle.left() <= self.ball.right() and
                paddle.top() >= self.ball.bottom() and
                paddle.bottom() <= self.ball.top())

    def handle_paddle_collision(self, paddle):
        """."""
        if self.collide_paddle(paddle):
            self.ball.color = (255, 0, 0)
            # self.ball.velocity.x = -self.ball.velocity.x
            scale = 1 - (1 * abs(self.ball.y - paddle.y) / (paddle.height // 2))
            # scale += 0.5
            print(scale)
            mag = self.ball.velocity.mag
            print(f"Speed: {max(1, min(2, mag*(scale+0.5)))}")
            # self.ball.velocity = self.ball.velocity.rotate(90)
            # self.ball.velocity.rotate(90),
            # self.ball.velocity = self.ball.velocity.lerp(
            #     Vec2(-self.ball.velocity.y,
            #          self.ball.velocity.x),
            #     alpha=scale
            # ).from_magnitude(mag)
            # self.ball.velocity = self.ball.velocity.reflect(
            #     Vec2(-self.ball.velocity.y,
            #          self.ball.velocity.x)
            # ).from_magnitude(mag*scale)
            self.ball.velocity = Vec2(0, 1).lerp(
                Vec2(self.ball.velocity.y,
                     -self.ball.velocity.x),
                alpha=scale
            ).from_magnitude(
                max(6, min(12, mag*(scale+0.5)))
            )
        else:
            self.ball.color = (255, 255, 255)

    def draw_ball(self):
        """."""
        self.ball.move()

        if self.ball.x <= self.width // 2:
            self.handle_paddle_collision(self.player1_paddle)
        else:
            self.handle_paddle_collision(self.player2_paddle)

        if self.collide_goal():
            self.ball.velocity.x = -self.ball.velocity.x

        if self.collide_table():
            # self.ball.velocity = self.ball.velocity.rotate(45)
            self.ball.velocity = Vec2(
                -self.ball.velocity.y,
                self.ball.velocity.x
            )

        self.ball.draw()

    def draw_paddles(self):
        """."""
        for symbol, ispressed in self.pressed.items():
            if ispressed:
                self.symbolevent[symbol]()
        self.player1_paddle.draw()
        self.player2_paddle.draw()

    def on_draw(self):
        """."""
        self.clear()

        # self.collide_paddle()
        # self.collide_bound()

        self.draw_paddles()
        self.draw_ball()

        self.linevec.x = self.ball.x
        self.linevec.y = self.ball.y
        self.linevec.x2 = self.ball.x - 15*self.ball.velocity.y
        self.linevec.y2 = self.ball.y + 15*self.ball.velocity.x

        self.linevec.draw()


pong = Pong(800, 600)
pyglet.app.run()
