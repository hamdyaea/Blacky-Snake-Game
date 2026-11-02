#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""Blacky Snake: testable grid game with optional Pygame frontend."""
from __future__ import annotations
import argparse
from dataclasses import dataclass, field
import random

WIDTH, HEIGHT, CELL = 72, 46, 10
DIRECTIONS = {"RIGHT": (1, 0), "LEFT": (-1, 0), "UP": (0, -1), "DOWN": (0, 1)}
OPPOSITES = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}

@dataclass
class Snake:
    body: list[tuple[int, int]] = field(default_factory=lambda: [(10, 5), (9, 5), (8, 5)])
    direction: str = "RIGHT"
    food: tuple[int, int] | None = None
    score: int = 0
    game_over: bool = False

    def __post_init__(self):
        if self.food is None:
            self.spawn_food()

    def spawn_food(self, rng=None) -> None:
        rng = rng or random
        occupied = set(self.body)
        free = [(x, y) for x in range(WIDTH) for y in range(HEIGHT) if (x, y) not in occupied]
        self.food = rng.choice(free) if free else None
        if self.food is None:
            self.game_over = True

    def turn(self, direction: str) -> None:
        if direction not in DIRECTIONS:
            raise ValueError("Invalid direction")
        if direction != OPPOSITES[self.direction]:
            self.direction = direction

    def step(self, rng=None) -> None:
        if self.game_over:
            return
        dx, dy = DIRECTIONS[self.direction]
        head = (self.body[0][0] + dx, self.body[0][1] + dy)
        growing = head == self.food
        collision_body = self.body if growing else self.body[:-1]
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT) or head in collision_body:
            self.game_over = True
            return
        self.body.insert(0, head)
        if growing:
            self.score += 1
            self.spawn_food(rng)
        else:
            self.body.pop()

def play(fps: int = 12) -> None:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * CELL, HEIGHT * CELL))
    pygame.display.set_caption("Blacky Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("sans", 26)
    snake = Snake()
    keys = {pygame.K_RIGHT: "RIGHT", pygame.K_LEFT: "LEFT", pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN", pygame.K_w: "UP", pygame.K_a: "LEFT",
            pygame.K_s: "DOWN", pygame.K_d: "RIGHT"}
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and snake.game_over:
                    snake = Snake()
                elif event.key in keys:
                    snake.turn(keys[event.key])
        if not snake.game_over:
            snake.step()
        screen.fill((245, 245, 245))
        for x, y in snake.body:
            pygame.draw.rect(screen, (45, 130, 90), (x * CELL, y * CELL, CELL, CELL))
        if snake.food:
            pygame.draw.rect(screen, (185, 60, 60), (snake.food[0] * CELL, snake.food[1] * CELL, CELL, CELL))
        screen.blit(font.render(f"Score: {snake.score}", True, (0, 0, 0)), (8, 8))
        if snake.game_over:
            screen.blit(font.render("Game over — press R to restart or Esc to quit", True, (180, 0, 0)), (80, 100))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fps", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.fps <= 60:
        parser.error("--fps must be between 1 and 60")
    play(args.fps)

if __name__ == "__main__":
    main()
