import math

import screen
from screen import Screen
import random
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = self.__generate_ship()
        self.__asteroids_amount = asteroids_amount
        self.__asteroids = self.__register_asteroids()
        self.__torpedos = []
        self.__ship_lives = 3
        self.__score = 0

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __generate_torpedo(self):
        if self.__screen.is_space_pressed():
            if len(self.__torpedos) < 10:
                torpedo_speed_x = self.__ship.get_speed_x() + (2 * math.cos(math.radians(self.__ship.get_heading())))
                torpedo_speed_y = self.__ship.get_speed_y() + (2 * math.sin(math.radians(self.__ship.get_heading())))
                torpedo = Torpedo(self.__ship.get_location_x(), torpedo_speed_x, self.__ship.get_location_y()
                                  , torpedo_speed_y, self.__ship.get_heading())
                self.__screen.register_torpedo(torpedo)
                self.__torpedos.append(torpedo)

    def __register_asteroids(self):
        asteroids = []
        for ast in range(self.__asteroids_amount):
                asteroids.append(self.__generate_asteroid())
                self.__screen.register_asteroid(asteroids[ast], asteroids[ast].get_size())
        return asteroids

    def __generate_asteroid(self):
        x = random.randrange(self.__screen_min_x, self.__screen_max_x)
        y = random.randrange(self.__screen_min_y, self.__screen_max_y)

        speed_x = random.randrange(1, 5) * random.choice([-1, 1])
        speed_y = random.randrange(1, 5) * random.choice([-1, 1])
        ast = Asteroid(x, y, speed_x, speed_y)
        return ast

    def __generate_ship(self):
        x = random.randrange(self.__screen_min_x, self.__screen_max_x)
        y = random.randrange(self.__screen_min_y, self.__screen_max_y)
        my_ship = Ship(x, y)
        return my_ship

    def object_movement(self, obj, old_spot_x, old_spot_y, speed_x, speed_y):
        delta = (self.__screen_max_x - self.__screen_min_x, self.__screen_max_y - self.__screen_min_y)
        new_spot_x = self.__screen_min_x + (old_spot_x + speed_x - self.__screen_min_x) % delta[0]
        new_spot_y = self.__screen_min_y + (old_spot_y + speed_y - self.__screen_min_y) % delta[1]
        obj.set_location(new_spot_x, new_spot_y)

    def change_heading_for_ship(self):
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(self.__ship.get_heading() - 7)

        if self.__screen.is_left_pressed():
            self.__ship.set_heading(self.__ship.get_heading() + 7)

    def accelerate_ship(self):

        if self.__screen.is_up_pressed():
            new_speed_x = self.__ship.get_speed_x() + math.cos(math.radians(self.__ship.get_heading()))
            new_speed_y = self.__ship.get_speed_y() + math.sin(math.radians(self.__ship.get_heading()))
            self.__ship.set_speed(new_speed_x, new_speed_y)

    def handle_movement_ship(self):

        self.object_movement(self.__ship, self.__ship.get_location_x(), self.__ship.get_location_y(),
                             self.__ship.get_speed_x(), self.__ship.get_speed_y())
        self.change_heading_for_ship()
        self.accelerate_ship()
        self.__screen.draw_ship(self.__ship.get_location_x(), self.__ship.get_location_y(), self.__ship.get_heading())

    def handle_movement_asteroid(self):
        for ast in self.__asteroids:
            self.object_movement(ast, ast.get_location_x(), ast.get_location_y(),
                                 ast.get_speed_x(), ast.get_speed_y())
            self.__screen.draw_asteroid(ast, ast.get_location_x(), ast.get_location_y())

    def handle_movement_torpedo(self):
        for torp in self.__torpedos:
            if not torp.is_dead():
                self.object_movement(torp, torp.get_location_x(), torp.get_location_y(), torp.get_speed_x(),
                                     torp.get_speed_y())
                self.__screen.draw_torpedo(torp, torp.get_location_x(), torp.get_location_y(), torp.get_heading())
                torp.update_life_span()
            else:
                self.__screen.unregister_torpedo(torp)
                self.__torpedos.remove(torp)

    def handle_movement(self):
        self.handle_movement_ship()

        self.handle_movement_asteroid()
        self.handle_movement_torpedo()

    def handle_exit(self):
        if self.__screen.should_end():
            self.__screen.show_message('End game', 'Thank you for playing')

            return True
        if self.__ship_lives == 0:
            self.__screen.show_message('YOU LOST', 'YOU ARE DEAD!')
            return True

        if not self.__asteroids:
            self.__screen.show_message('YOU WON', 'You are the king of the game!')
            return True
        else:
            return False

    def _game_loop(self):
        # TODO: Your code goes here
        self.handle_movement()
        self.handle_intersection()
        self.__generate_torpedo()
        if self.handle_exit():
            self.__screen.end_game()
            sys.exit

    def __calculate_speed_for_spliting_asts(self, ast, torp):
        new_asteroids_speed_x = (torp.get_speed_x() + ast.get_speed_x()) / \
                                (math.sqrt(math.pow(ast.get_speed_y(), 2) + math.pow(ast.get_speed_x(), 2)))
        new_asteroids_speed_y = (torp.get_speed_y() + ast.get_speed_y()) / \
                                (math.sqrt(math.pow(ast.get_speed_y(), 2) + math.pow(ast.get_speed_x(), 2)))
        return new_asteroids_speed_x, new_asteroids_speed_y

    def split_asteroid(self, ast, torp):
        new_asteroids_speed_x, new_asteroids_speed_y = self.__calculate_speed_for_spliting_asts(ast, torp)
        ast1 = Asteroid(ast.get_location_x(), ast.get_location_y(), new_asteroids_speed_x,
                        new_asteroids_speed_y, ast.get_size() - 1)
        ast2 = Asteroid(ast.get_location_x(), ast.get_location_y(), (-1) * new_asteroids_speed_x,
                        (-1) * new_asteroids_speed_y, ast.get_size() - 1)
        self.__asteroids.append(ast1)
        self.__screen.register_asteroid(ast1, ast1.get_size())
        self.__asteroids.append(ast2)
        self.__screen.register_asteroid(ast2, ast2.get_size())

    def handle_intersection(self):
        for ast in self.__asteroids:
            if ast.has_intersection(self.__ship):
                self.__screen.show_message('boom', "BOOM!!")
                self.__screen.unregister_asteroid(ast)
                self.__asteroids.remove(ast)
                self.__ship_lives -= 1
                self.__screen.remove_life()
            for torp in self.__torpedos:
                if ast.has_intersection(torp):
                    self.__screen.show_message('kabam', "KABAM!!!!")
                    if ast.get_size() == 3:
                        self.split_asteroid(ast, torp)
                        self.__score += 20
                        self.__screen.set_score(self.__score)
                    if ast.get_size() == 2:
                        self.split_asteroid(ast, torp)
                        self.__score += 50
                        self.__screen.set_score(self.__score)
                    if ast.get_size() == 1:
                        self.__score += 100
                        self.__screen.set_score(self.__score)
                    self.__screen.unregister_asteroid(ast)
                    self.__asteroids.remove(ast)
                    self.__screen.unregister_torpedo(torp)
                    self.__torpedos.remove(torp)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
