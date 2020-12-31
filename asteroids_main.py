################################################################
# FILE : ex10.py
# WRITER1 : Ido Pinto , idopinto12 , 206483620
# WRITER2 : Eilon Yaacov , eilon277 , 208562405
# EXERCISE : intro2cs2 ex10 2020
# DESCRIPTION: this program is an asteroids game.
#################################################################
import math

import screen
from screen import Screen
import random
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys

DEFAULT_ASTEROIDS_NUM = 3


class GameRunner:
    """The class GameRunner is a
    the class is familiar with the classes ship, torpedo, asteroid and screen.
    The constructor of the the class gets the amount of asteroids in the game. is it didn't get anything,
    it will use the default amount which is 3 asteroids.
     Th constructor holds the game screen, the ship, the asteroids, the torpedoes,
     the lives and the score in the game."""

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
        """This method is responsible to run of the game, means it
        runs the game loops."""
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """This method is responsible for a single run of the game, means it
            runs the one game loop and update the screen."""
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __generate_torpedo(self):
        """This method the responsible for the torpedoes the ship fires."""
        if self.__screen.is_space_pressed():
            if len(self.__torpedos) < 10:  # as long as there aren't already 10 torpedoes on the screen
                torpedo_speed_x = self.__ship.get_speed_x() + (2 * math.cos(math.radians(self.__ship.get_heading())))
                torpedo_speed_y = self.__ship.get_speed_y() + (2 * math.sin(math.radians(self.__ship.get_heading())))
                torpedo = Torpedo(self.__ship.get_location_x(), torpedo_speed_x, self.__ship.get_location_y()
                                  , torpedo_speed_y, self.__ship.get_heading())
                self.__screen.register_torpedo(torpedo)  # adds the torpedo to the screen
                self.__torpedos.append(torpedo)  # adds the torpedo to the current torpedoes
                # list the ship as already fired and still on the screen.

    def __register_asteroids(self):
        """This method adds the screen the asteroids provided to start the game with."""
        asteroids = []
        for ast in range(self.__asteroids_amount):
            asteroids.append(self.__generate_asteroid())
            self.__screen.register_asteroid(asteroids[ast], asteroids[ast].get_size())
        return asteroids

    def __generate_asteroid(self):
        """This method generate a random asteroid. the method gets nothing and returns an asteroid."""
        x = random.randrange(self.__screen_min_x, self.__screen_max_x)
        y = random.randrange(self.__screen_min_y, self.__screen_max_y)
        if x != self.__ship.get_location_x() and y != self.__ship.get_location_y():
            speed_x = random.randrange(1, 5) * random.choice([-1, 1])  # random speed between -4 to 4, zero not included
            speed_y = random.randrange(1, 5) * random.choice([-1, 1])  # random speed between -4 to 4, zero not included
            ast = Asteroid(x, y, speed_x, speed_y)
        else:
            while x == self.__ship.get_location_x() and y == self.__ship.get_location_y():
                x = random.randrange(self.__screen_min_x, self.__screen_max_x)
                y = random.randrange(self.__screen_min_y, self.__screen_max_y)
                if x != self.__ship.get_location_x() and y != self.__ship.get_location_y():
                    speed_x = random.randrange(1, 5) * random.choice(
                        [-1, 1])  # random speed between -4 to 4, zero not included
                    speed_y = random.randrange(1, 5) * random.choice(
                        [-1, 1])  # random speed between -4 to 4, zero not included
                    ast = Asteroid(x, y, speed_x, speed_y)
        return ast

    def __generate_ship(self):
        """This method generate the ship of the game. it gets nothing and returns the ship.
        the ship's location on the screen is random."""
        x = random.randrange(self.__screen_min_x, self.__screen_max_x)
        y = random.randrange(self.__screen_min_y, self.__screen_max_y)
        my_ship = Ship(x, y)
        return my_ship

    def object_movement(self, obj, old_spot_x, old_spot_y, speed_x, speed_y):
        """This method is responsible for the data for the movement of all objects on the screen.
        The method gets the object, the object location and speed and sets the new location.
        The method returns nothing."""
        delta = (self.__screen_max_x - self.__screen_min_x, self.__screen_max_y - self.__screen_min_y)
        new_spot_x = self.__screen_min_x + (old_spot_x + speed_x - self.__screen_min_x) % delta[0]
        new_spot_y = self.__screen_min_y + (old_spot_y + speed_y - self.__screen_min_y) % delta[1]
        obj.set_location(new_spot_x,
                         new_spot_y)  # regardless the object, weather it's a ship, an asteroid or a torpedo.

    def change_heading_for_ship(self):
        """This method changes the direction the ship is heading to according to the bottom pressed by the player.
         the method gets nothing ans returns nothing."""
        if self.__screen.is_right_pressed():
            self.__ship.set_heading(self.__ship.get_heading() - 7)

        if self.__screen.is_left_pressed():
            self.__ship.set_heading(self.__ship.get_heading() + 7)

    def accelerate_ship(self):
        """This method accelerate the ship's speed towards the direction it was heading to.
        in case the up bottom were pressed.
        The method gets and returns nothing."""
        if self.__screen.is_up_pressed():
            new_speed_x = self.__ship.get_speed_x() + math.cos(
                math.radians(self.__ship.get_heading()))  # the ship heading in radians.
            new_speed_y = self.__ship.get_speed_y() + math.sin(
                math.radians(self.__ship.get_heading()))  # the ship heading in radians.
            self.__ship.set_speed(new_speed_x, new_speed_y)

    def handle_movement_ship(self):
        """This method is responsible for the movement of the ship on the screen.
        The method gets nothing and returns nothing. """
        self.object_movement(self.__ship, self.__ship.get_location_x(), self.__ship.get_location_y(),
                             self.__ship.get_speed_x(), self.__ship.get_speed_y())
        self.change_heading_for_ship()  # in case the player pressed right or left
        self.accelerate_ship()  # in case the player pressed up
        self.__screen.draw_ship(self.__ship.get_location_x(), self.__ship.get_location_y(), self.__ship.get_heading())

    def handle_movement_asteroid(self):
        """This method is responsible for the movement of the asteroids on the screen.
        The method gets nothing and returns nothing. """
        for ast in self.__asteroids:  # for every asteroid in the game
            self.object_movement(ast, ast.get_location_x(), ast.get_location_y(),
                                 ast.get_speed_x(), ast.get_speed_y())
            self.__screen.draw_asteroid(ast, ast.get_location_x(), ast.get_location_y())

    def handle_movement_torpedo(self):
        """This method is responsible for the movement of the torpedoes on the screen.
        The method gets nothing and returns nothing. """
        for torp in self.__torpedos:  # for every torpedo in the game
            if not torp.is_dead():  # as long as the torpedo is still alive
                self.object_movement(torp, torp.get_location_x(), torp.get_location_y(), torp.get_speed_x(),
                                     torp.get_speed_y())
                self.__screen.draw_torpedo(torp, torp.get_location_x(), torp.get_location_y(), torp.get_heading())
                torp.update_life_span()
            else:
                self.__screen.unregister_torpedo(torp)  # if the torpedo is dead, this will remove it from the screen
                self.__torpedos.remove(torp)  # removes it from the list of torpedoes.

    def handle_movement(self):
        """This method is responsible for the movement of all objects on the screen.
        The method gets nothing and returns nothing. """
        self.handle_movement_ship()

        self.handle_movement_asteroid()
        self.handle_movement_torpedo()

    def handle_exit(self):
        """This method is responsible to end the game.
        It gets nothing, and returns True if the game is over and False otherwise."""
        if self.__screen.should_end():  # in case the player pressed q
            self.__screen.show_message('End game', 'Thank you for playing')

            return True
        if self.__ship_lives == 0:  # in case the player ran out of lives
            self.__screen.show_message('YOU LOST', 'YOU ARE DEAD!')
            return True

        if not self.__asteroids:  # in case all the asteroids were destroyed.
            self.__screen.show_message('YOU WON', 'You are the king of the game!')
            return True
        else:
            return False

    def __calculate_speed_for_spliting_asts(self, ast, torp):
        """This method is responsible for the data of the speed to split an asteroid if it gets hit by a torpedo.
         The method gets the asteroid the was being hit and the torpedo that hit it and returns the new speed
         of the new asteroids after the hit."""
        new_asteroids_speed_x = (torp.get_speed_x() + ast.get_speed_x()) / \
                                (math.sqrt(math.pow(ast.get_speed_y(), 2) + math.pow(ast.get_speed_x(), 2)))
        new_asteroids_speed_y = (torp.get_speed_y() + ast.get_speed_y()) / \
                                (math.sqrt(math.pow(ast.get_speed_y(), 2) + math.pow(ast.get_speed_x(), 2)))
        return new_asteroids_speed_x, new_asteroids_speed_y

    def split_asteroid(self, ast, torp):
        """This method is responsible to split an asteroid if it gets hit by a torpedo.
         The method gets the asteroid the was being hit and the torpedo that hit it."""
        new_asteroids_speed_x, new_asteroids_speed_y = self.__calculate_speed_for_spliting_asts(ast, torp)
        ast1 = Asteroid(ast.get_location_x(), ast.get_location_y(), new_asteroids_speed_x,
                        new_asteroids_speed_y,
                        ast.get_size() - 1)  # the first asteroid is created with positive speed.
        ast2 = Asteroid(ast.get_location_x(), ast.get_location_y(), (-1) * new_asteroids_speed_x,
                        (-1) * new_asteroids_speed_y,
                        ast.get_size() - 1)  # the first asteroid is created with negative speed
        self.__asteroids.append(ast1)  # adds the first asteroid to the asteroids list
        self.__screen.register_asteroid(ast1, ast1.get_size())  # adds the asteroid to the screen
        self.__asteroids.append(ast2)  # adds the second asteroid to the asteroids list
        self.__screen.register_asteroid(ast2, ast2.get_size())  # adds the asteroid to the screen

    def handle_intersection(self):
        """This methods is responsible for the intersections on the screen between objects."""
        for ast in self.__asteroids:  # for all asteroids
            if ast.has_intersection(self.__ship):  # if the asteroid hit the ship
                self.__screen.show_message('boom', "BOOM!!")
                self.__screen.unregister_asteroid(ast)  # the asteroid is dead and is removed from the screen and list.
                self.__asteroids.remove(ast)
                self.__ship_lives -= 1  # the ship loses life
                self.__screen.remove_life()
            for torp in self.__torpedos:  # for all torpedoes
                if ast.has_intersection(torp):  # if the asteroid hit a torpedo
                    self.__screen.show_message('kabam', "KABAM!!!!")
                    if ast.get_size() == 3:  # if the asteroid size is 3
                        self.split_asteroid(ast, torp)
                        self.__score += 20
                        self.__screen.set_score(self.__score)
                    if ast.get_size() == 2:  # if the asteroid size is 2
                        self.split_asteroid(ast, torp)
                        self.__score += 50
                        self.__screen.set_score(self.__score)
                    if ast.get_size() == 1:  # if the asteroid size is 1, we don't call the split method.
                        self.__score += 100
                        self.__screen.set_score(self.__score)
                    self.__screen.unregister_asteroid(ast)  # removes the asteroid from the screen
                    self.__asteroids.remove(ast)
                    self.__screen.unregister_torpedo(torp)  # removes the torpedo from the screen
                    self.__torpedos.remove(torp)

    def _game_loop(self):
        """This method runs the game loop.
        basically, this is the most important method, since it is the method the makes it look like a game. 
        almost all methods are being called when we call this method."""""
        self.handle_movement()
        self.handle_intersection()
        self.__generate_torpedo()
        if self.handle_exit():
            self.__screen.end_game()
            sys.exit()


def main(amount):
    """This function runs the game. it gets the amount of asteroids to start the game with."""
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
