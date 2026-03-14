import random
import time
import turtle
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
 
 
class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
 
 
@dataclass(frozen=True)
class SnakeStyle:
    scale: float
    head_scale: float
    head_color: Tuple[int, int, int]
    head_outline: Tuple[int, int, int]
    body_color_start: Tuple[int, int, int]
    body_color_end: Tuple[int, int, int]
    body_outline: Tuple[int, int, int]
    eye_enabled: bool
    eye_color: Tuple[int, int, int]
    pupil_color: Tuple[int, int, int]
    eye_scale: float
 
 
@dataclass(frozen=True)
class Settings:
    width: int = 1200
    height: int = 1200
    step: int = 20
    initial_length: int = 3
    initial_delay_s: float = 0.12
    min_delay_s: float = 0.04
    speedup_per_food: float = 0.003
    grid_enabled: bool = True
    grid_color: str = "#202020"
    grid_line_width: int = 1
    border_enabled: bool = True
    border_color: str = "#404040"
    border_line_width: int = 2
    p1_style: SnakeStyle = field(
        default_factory=lambda: SnakeStyle(
            scale=0.9,
            head_scale=0.98,
            head_color=(40, 255, 140),
            head_outline=(10, 80, 40),
            body_color_start=(20, 210, 110),
            body_color_end=(10, 120, 60),
            body_outline=(10, 70, 35),
            eye_enabled=True,
            eye_color=(245, 245, 245),
            pupil_color=(20, 20, 20),
            eye_scale=0.22,
        )
    )
    p2_style: SnakeStyle = field(
        default_factory=lambda: SnakeStyle(
            scale=0.9,
            head_scale=0.98,
            head_color=(80, 190, 255),
            head_outline=(20, 60, 90),
            body_color_start=(60, 160, 245),
            body_color_end=(30, 90, 160),
            body_outline=(15, 45, 75),
            eye_enabled=True,
            eye_color=(245, 245, 245),
            pupil_color=(20, 20, 20),
            eye_scale=0.22,
        )
    )
 
 
class Grid:
    def __init__(
        self,
        width: int,
        height: int,
        step: int,
        color: str,
        line_width: int,
        border_enabled: bool,
        border_color: str,
        border_line_width: int,
    ) -> None:
        self._width = width
        self._height = height
        self._step = step
        self._color = color
        self._line_width = line_width
        self._border_enabled = border_enabled
        self._border_color = border_color
        self._border_line_width = border_line_width
        self._pen = turtle.Turtle(visible=False)
        self._pen.speed(0)
        self._pen.penup()
        self.draw()
 
    def draw(self) -> None:
        self._pen.clear()
        max_x = self._width // 2 - self._step
        max_y = self._height // 2 - self._step
 
        self._pen.color(self._color)
        self._pen.pensize(self._line_width)
        for x in range(-max_x, max_x + 1, self._step):
            self._pen.goto(x, -max_y)
            self._pen.pendown()
            self._pen.goto(x, max_y)
            self._pen.penup()
 
        for y in range(-max_y, max_y + 1, self._step):
            self._pen.goto(-max_x, y)
            self._pen.pendown()
            self._pen.goto(max_x, y)
            self._pen.penup()
 
        if self._border_enabled:
            self._pen.color(self._border_color)
            self._pen.pensize(self._border_line_width)
            self._pen.goto(-max_x, -max_y)
            self._pen.pendown()
            self._pen.goto(max_x, -max_y)
            self._pen.goto(max_x, max_y)
            self._pen.goto(-max_x, max_y)
            self._pen.goto(-max_x, -max_y)
            self._pen.penup()
 
 
class Snake:
    def __init__(
        self,
        step: int,
        initial_length: int,
        style: SnakeStyle,
        start_pos: Tuple[int, int],
        direction: Direction,
    ) -> None:
        self._step = step
        self._style = style
        self._segments: List[turtle.Turtle] = []
        self._direction = direction
        self._pending_growth = 0
        self._eyes: List[turtle.Turtle] = []
        self._pupils: List[turtle.Turtle] = []
        self._start_pos = start_pos
        self._start_direction = direction
        self._build(initial_length, start_pos, direction)
        self._build_eyes()
        self.update_visuals()
 
    @property
    def head(self) -> turtle.Turtle:
        return self._segments[0]
 
    @property
    def direction(self) -> Direction:
        return self._direction
 
    def set_direction(self, direction: Direction) -> None:
        if self._is_opposite(direction, self._direction):
            return
        self._direction = direction
 
    def positions(self) -> List[Tuple[float, float]]:
        return [(s.xcor(), s.ycor()) for s in self._segments]
 
    def next_head_position(self) -> Tuple[float, float]:
        dx, dy = self._direction.value
        return (self.head.xcor() + dx * self._step, self.head.ycor() + dy * self._step)
 
    def advance_to(self, next_x: float, next_y: float) -> None:
        if self._pending_growth > 0:
            self._pending_growth -= 1
            tail = self._segments[-1]
            segment = self._new_segment(tail.xcor(), tail.ycor())
            self._segments.append(segment)
 
        for i in range(len(self._segments) - 1, 0, -1):
            self._segments[i].goto(self._segments[i - 1].xcor(), self._segments[i - 1].ycor())
        self.head.goto(next_x, next_y)
        self.update_visuals()
 
    def grow(self, amount: int = 1) -> None:
        self._pending_growth += max(0, amount)
 
    def collided_with_self(self) -> bool:
        hx, hy = self.head.xcor(), self.head.ycor()
        for x, y in self.positions()[1:]:
            if abs(hx - x) < self._step / 2 and abs(hy - y) < self._step / 2:
                return True
        return False
 
    def reset(self, initial_length: int, start_pos: Optional[Tuple[int, int]] = None, direction: Optional[Direction] = None) -> None:
        for s in self._segments:
            s.hideturtle()
        for e in self._eyes:
            e.hideturtle()
        for p in self._pupils:
            p.hideturtle()
        self._segments.clear()
        self._eyes.clear()
        self._pupils.clear()
        start_pos = start_pos if start_pos is not None else self._start_pos
        direction = direction if direction is not None else self._start_direction
        self._start_pos = start_pos
        self._start_direction = direction
        self._direction = direction
        self._pending_growth = 0
        self._build(initial_length, start_pos, direction)
        self._build_eyes()
        self.update_visuals()
 
    def _build(self, initial_length: int, start_pos: Tuple[int, int], direction: Direction) -> None:
        dx, dy = direction.value
        start_x, start_y = start_pos
        for i in range(initial_length):
            x = start_x - dx * self._step * i
            y = start_y - dy * self._step * i
            self._segments.append(self._new_segment(x, y))
 
    def _new_segment(self, x: float, y: float) -> turtle.Turtle:
        t = turtle.Turtle("square")
        t.speed(0)
        t.penup()
        t.goto(x, y)
        return t
 
    def _is_opposite(self, a: Direction, b: Direction) -> bool:
        ax, ay = a.value
        bx, by = b.value
        return ax == -bx and ay == -by
 
    def update_visuals(self) -> None:
        self._apply_colors_and_sizes()
        self._position_eyes()
 
    def _apply_colors_and_sizes(self) -> None:
        if not self._segments:
            return
 
        head = self._segments[0]
        head.shape("triangle")
        head.color(self._style.head_outline, self._style.head_color)
        head.shapesize(self._style.head_scale, self._style.head_scale)
        if self._direction == Direction.RIGHT:
            head.setheading(0)
        elif self._direction == Direction.UP:
            head.setheading(90)
        elif self._direction == Direction.LEFT:
            head.setheading(180)
        else:
            head.setheading(270)
 
        n = len(self._segments)
        if n <= 1:
            return
 
        sr, sg, sb = self._style.body_color_start
        er, eg, eb = self._style.body_color_end
        for i in range(1, n):
            t = i / (n - 1)
            r = int(sr + (er - sr) * t)
            g = int(sg + (eg - sg) * t)
            b = int(sb + (eb - sb) * t)
            self._segments[i].shape("square")
            self._segments[i].color(self._style.body_outline, (r, g, b))
            self._segments[i].shapesize(self._style.scale, self._style.scale)
 
    def _build_eyes(self) -> None:
        if not self._style.eye_enabled:
            return
        for _ in range(2):
            eye = turtle.Turtle("circle")
            eye.speed(0)
            eye.penup()
            eye.color(self._style.eye_color, self._style.eye_color)
            eye.shapesize(self._style.eye_scale, self._style.eye_scale)
            self._eyes.append(eye)
 
            pupil = turtle.Turtle("circle")
            pupil.speed(0)
            pupil.penup()
            pupil.color(self._style.pupil_color, self._style.pupil_color)
            pupil.shapesize(self._style.eye_scale * 0.55, self._style.eye_scale * 0.55)
            self._pupils.append(pupil)
 
    def _position_eyes(self) -> None:
        if not self._eyes or not self._pupils:
            return
 
        x = self.head.xcor()
        y = self.head.ycor()
        step = self._step
        front = step * 0.22
        side = step * 0.18
 
        if self._direction == Direction.RIGHT:
            positions = [(x + front, y + side), (x + front, y - side)]
            pupil_positions = [(x + front + step * 0.05, y + side), (x + front + step * 0.05, y - side)]
        elif self._direction == Direction.LEFT:
            positions = [(x - front, y + side), (x - front, y - side)]
            pupil_positions = [(x - front - step * 0.05, y + side), (x - front - step * 0.05, y - side)]
        elif self._direction == Direction.UP:
            positions = [(x - side, y + front), (x + side, y + front)]
            pupil_positions = [(x - side, y + front + step * 0.05), (x + side, y + front + step * 0.05)]
        else:
            positions = [(x - side, y - front), (x + side, y - front)]
            pupil_positions = [(x - side, y - front - step * 0.05), (x + side, y - front - step * 0.05)]
 
        for eye, (ex, ey) in zip(self._eyes, positions):
            eye.goto(ex, ey)
        for pupil, (px, py) in zip(self._pupils, pupil_positions):
            pupil.goto(px, py)
 
 
class Food:
    def __init__(self, step: int, bounds: Tuple[int, int]) -> None:
        self._step = step
        self._max_x, self._max_y = bounds
        self.turtle = turtle.Turtle("circle")
        self.turtle.speed(0)
        self.turtle.color((120, 20, 20), (255, 70, 70))
        self.turtle.shapesize(0.75, 0.75)
        self.turtle.penup()
        self.relocate([])
 
    def relocate(self, blocked_positions: List[Tuple[float, float]]) -> None:
        blocked = set((int(x), int(y)) for x, y in blocked_positions)
        for _ in range(2000):
            x = random.randrange(-self._max_x, self._max_x + 1, self._step)
            y = random.randrange(-self._max_y, self._max_y + 1, self._step)
            if (x, y) not in blocked:
                self.turtle.goto(x, y)
                return
        self.turtle.goto(0, 0)
 
 
class Scoreboard:
    def __init__(self, width: int, height: int) -> None:
        self._p1 = 0
        self._p2 = 0
        self._banner = turtle.Turtle(visible=False)
        self._banner.color("white")
        self._banner.penup()
        self._banner.goto(0, height // 2 - 40)
        self._status = turtle.Turtle(visible=False)
        self._status.color("white")
        self._status.penup()
        self._status.goto(0, 0)
        self.draw()
 
    @property
    def p1_score(self) -> int:
        return self._p1
 
    @property
    def p2_score(self) -> int:
        return self._p2
 
    def add_p1(self, amount: int = 1) -> None:
        self._p1 += amount
        self.draw()
 
    def add_p2(self, amount: int = 1) -> None:
        self._p2 += amount
        self.draw()
 
    def reset(self) -> None:
        self._p1 = 0
        self._p2 = 0
        self.draw()
 
    def draw(self) -> None:
        self._banner.clear()
        self._banner.write(f"P1: {self._p1}    P2: {self._p2}", align="center", font=("Courier", 18, "normal"))
 
    def show_message(self, text: str, seconds: float = 1.2) -> None:
        self._status.clear()
        self._status.write(text, align="center", font=("Courier", 18, "normal"))
        self._status.getscreen().update()
        time.sleep(max(0.0, seconds))
        self._status.clear()
 
 
class Game:
    def __init__(self, settings: Settings) -> None:
        self._s = settings
        self._screen = turtle.Screen()
        self._screen.setup(width=settings.width, height=settings.height)
        self._screen.title("Snake Game (Python)")
        self._screen.bgcolor("black")
        self._screen.tracer(0)
        self._screen.colormode(255)
 
        self._world_width = self._screen.window_width()
        self._world_height = self._screen.window_height()
 
        max_x = self._world_width // 2 - settings.step
        max_y = self._world_height // 2 - settings.step
 
        self._grid = None
        if settings.grid_enabled:
            self._grid = Grid(
                width=self._world_width,
                height=self._world_height,
                step=settings.step,
                color=settings.grid_color,
                line_width=settings.grid_line_width,
                border_enabled=settings.border_enabled,
                border_color=settings.border_color,
                border_line_width=settings.border_line_width,
            )
 
        p1_start = (-settings.step * 5, 0)
        p2_start = (settings.step * 5, 0)
        self._snake1 = Snake(
            step=settings.step,
            initial_length=settings.initial_length,
            style=settings.p1_style,
            start_pos=p1_start,
            direction=Direction.RIGHT,
        )
        self._snake2 = Snake(
            step=settings.step,
            initial_length=settings.initial_length,
            style=settings.p2_style,
            start_pos=p2_start,
            direction=Direction.LEFT,
        )
        self._food = Food(step=settings.step, bounds=(max_x, max_y))
        self._scoreboard = Scoreboard(width=self._world_width, height=self._world_height)
        self._food.relocate(self._snake1.positions() + self._snake2.positions())
 
        self._delay_s = settings.initial_delay_s
        self._paused = False
        self._running = True
 
        self._bind_keys()
        self._screen.listen()
 
    def run(self) -> None:
        while self._running:
            self._screen.update()
            if not self._paused:
                self._tick()
            time.sleep(self._delay_s)
        try:
            self._screen.bye()
        except turtle.Terminator:
            return
 
    def _tick(self) -> None:
        next1 = self._wrap_position(*self._snake1.next_head_position())
        next2 = self._wrap_position(*self._snake2.next_head_position())
 
        p1_body = set((int(x), int(y)) for x, y in self._snake1.positions()[1:])
        p2_body = set((int(x), int(y)) for x, y in self._snake2.positions()[1:])
        p1_all = set((int(x), int(y)) for x, y in self._snake1.positions())
        p2_all = set((int(x), int(y)) for x, y in self._snake2.positions())
 
        next1_cell = (int(next1[0]), int(next1[1]))
        next2_cell = (int(next2[0]), int(next2[1]))
 
        p1_lost = next1_cell in p1_body or next1_cell in p2_all or next1_cell == next2_cell
        p2_lost = next2_cell in p2_body or next2_cell in p1_all or next1_cell == next2_cell
 
        if p1_lost and p2_lost:
            self._scoreboard.show_message("Both crashed!", seconds=1.0)
            self.reset()
            return
        if p1_lost:
            self._scoreboard.show_message("P1 crashed!", seconds=1.0)
            self.reset()
            return
        if p2_lost:
            self._scoreboard.show_message("P2 crashed!", seconds=1.0)
            self.reset()
            return
 
        self._snake1.advance_to(*next1)
        self._snake2.advance_to(*next2)
 
        ate1 = self._snake1.head.distance(self._food.turtle) < self._s.step * 0.75
        ate2 = self._snake2.head.distance(self._food.turtle) < self._s.step * 0.75
        if ate1:
            self._snake1.grow(1)
            self._scoreboard.add_p1(1)
        if ate2:
            self._snake2.grow(1)
            self._scoreboard.add_p2(1)
        if ate1 or ate2:
            self._food.relocate(self._snake1.positions() + self._snake2.positions())
            eaten = (1 if ate1 else 0) + (1 if ate2 else 0)
            self._delay_s = max(self._s.min_delay_s, self._delay_s - self._s.speedup_per_food * eaten)
 
    def reset(self) -> None:
        p1_start = (-self._s.step * 5, 0)
        p2_start = (self._s.step * 5, 0)
        self._snake1.reset(self._s.initial_length, start_pos=p1_start, direction=Direction.RIGHT)
        self._snake2.reset(self._s.initial_length, start_pos=p2_start, direction=Direction.LEFT)
        self._food.relocate(self._snake1.positions() + self._snake2.positions())
        self._scoreboard.reset()
        self._delay_s = self._s.initial_delay_s
        self._paused = False
 
    def _toggle_pause(self) -> None:
        self._paused = not self._paused
 
    def _quit(self) -> None:
        self._running = False
 
    def _bind_keys(self) -> None:
        self._screen.onkey(lambda: self._snake1.set_direction(Direction.UP), "Up")
        self._screen.onkey(lambda: self._snake1.set_direction(Direction.DOWN), "Down")
        self._screen.onkey(lambda: self._snake1.set_direction(Direction.LEFT), "Left")
        self._screen.onkey(lambda: self._snake1.set_direction(Direction.RIGHT), "Right")
 
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.UP), "w")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.DOWN), "s")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.LEFT), "a")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.RIGHT), "d")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.UP), "W")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.DOWN), "S")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.LEFT), "A")
        self._screen.onkey(lambda: self._snake2.set_direction(Direction.RIGHT), "D")
        self._screen.onkey(self._toggle_pause, "p")
        self._screen.onkey(self._toggle_pause, "P")
        self._screen.onkey(self.reset, "r")
        self._screen.onkey(self.reset, "R")
        self._screen.onkey(self._quit, "q")
        self._screen.onkey(self._quit, "Q")
        self._screen.onkey(self._quit, "Escape")
 
    def _wrap_position(self, x: float, y: float) -> Tuple[float, float]:
        max_x = self._world_width // 2 - self._s.step
        max_y = self._world_height // 2 - self._s.step
 
        wrapped_x = x
        wrapped_y = y
 
        if x > max_x:
            wrapped_x = -max_x
        elif x < -max_x:
            wrapped_x = max_x
 
        if y > max_y:
            wrapped_y = -max_y
        elif y < -max_y:
            wrapped_y = max_y
 
        return (wrapped_x, wrapped_y)
 
 
def main() -> None:
    Game(Settings()).run()
 
 
if __name__ == "__main__":
    main()
