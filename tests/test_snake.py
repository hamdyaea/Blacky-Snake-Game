# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("snake", Path(__file__).resolve().parents[1] / "Blacky-Snake-Game.py")
snake = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = snake
spec.loader.exec_module(snake)

class SnakeTests(unittest.TestCase):
    def test_move(self):
        game = snake.Snake(food=(0, 0))
        game.step()
        self.assertEqual(game.body[0], (11, 5))
        self.assertEqual(len(game.body), 3)
    def test_prevent_reverse(self):
        game = snake.Snake(food=(0, 0))
        game.turn("LEFT")
        self.assertEqual(game.direction, "RIGHT")
    def test_food_growth(self):
        game = snake.Snake(food=(11, 5))
        game.step()
        self.assertEqual(game.score, 1)
        self.assertEqual(len(game.body), 4)
        self.assertNotIn(game.food, game.body)
    def test_wall_collision(self):
        game = snake.Snake(body=[(71, 0)], food=(0, 0))
        game.step()
        self.assertTrue(game.game_over)

if __name__ == "__main__":
    unittest.main()
