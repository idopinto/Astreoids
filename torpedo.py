class Torpedo:

    def __init__(self, location_x, speed_x, location_y, speed_y, heading):
        self.__location_X = location_x
        self.__speed_X = speed_x
        self.__speed_Y = speed_y
        self.__location_Y = location_y
        self.__heading = heading
        self.__radius = 4
        self.__life_span = 0

    def update_life_span(self):
        self.__life_span += 1

    def is_dead(self):
        return self.__life_span == 200

    def get_radius(self):
        return self.__radius


    def get_location_x(self):
        return self.__location_X

    def get_speed_x(self):
        return self.__speed_X

    def get_location_y(self):
        return self.__location_Y

    def get_speed_y(self):
        return self.__speed_Y

    def get_heading(self):
        return self.__heading

    def set_location(self, new_location_for_x, new_location_for_y):
        self.__location_X = new_location_for_x
        self.__location_Y = new_location_for_y

    def set_speed(self, new_speed_for_x, new_speed_for_y):
        self.__speed_X = new_speed_for_x
        self.__speed_Y = new_speed_for_y

    def set_heading(self, new_heading):
        self.__heading = new_heading