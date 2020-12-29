import math


class Asteroid:

    def __init__(self, location_x, location_y, speed_x, speed_y, size=3):
        self.__location_x = location_x
        self.__location_y = location_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__size = size
        self.__radius = size * 10 - 5

    def has_intersection(self, obj):
        distance = math.sqrt(math.pow(obj.get_location_x() - self.__location_x,2)
                             + math.pow(obj.get_location_y() - self.__location_y,2))
        if distance <= self.__radius + obj.get_radius():
            return True
        return False


    # getters

    def get_location_x(self):
        return self.__location_x

    def get_location_y(self):
        return self.__location_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def get_size(self):
        return self.__size

    def get_radius(self):
        return self.__radius

    # SETTERS
    def set_location(self, x, y):
        self.__location_x = x
        self.__location_y = y

    def set_speed(self, x, y):
        self.__speed_x = x
        self.__speed_y = y

    def set_size(self, new_size):
        self.__size = new_size
