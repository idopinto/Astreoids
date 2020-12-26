class Ship:

    def _init_(self, location_x, speed_x, location_y,speed_y, direction):
        self.__location_X = location_x
        self.__speed_X = speed_x

        self.__speed_Y = speed_y
        self.__location_Y = location_y
        self.__direction = direction

    def get_location_x(self):
        return self.__location_X

    def get_speed_x(self):

        return self.__speed_X

    def get_location_y(self):
        return self.__location_Y

    def get_speed_y(self):
        return self.__speed_Y

    def get_direction(self):
        return self.__speed_X

    def set_location_x(self,new_location_for_x):
        self.__location_X = new_location_for_x

    def set_location_y(self,new_location_for_y):
        self.__location_Y = new_location_for_y

    def set_speed_x(self, new_speed_for_x):
        self.__speed_X = new_speed_for_x

    def set_speed_y(self,new_speed_for_y):
        self.__speed_Y = new_speed_for_y

    def set_direction(self, new_direction):
        self.__direction = new_direction