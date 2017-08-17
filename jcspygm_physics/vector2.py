#  ========================================================================
#  $File: vector2.py $
#  $Date: 2017-02-01 05:49:56 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================

import physics
import math


class Vector2(object):
    """
    @class Vector2
    @brief Vector with 2 float.
    """

    # --------------------------------------------
    # Public Variables
    # --------------------------------------------

    # --------------------------------------------
    # Private Variables
    # --------------------------------------------

    # --------------------------------------------
    # Protected Variables
    # --------------------------------------------

    # --------------------------------------------
    # Constructor
    # --------------------------------------------
    def __init__(self, x = 0, y = 0):
        """Constructor."""

        self.x = x
        self.y = y

    # --------------------------------------------
    # Public Methods
    # --------------------------------------------
    def normalize(self):
        """Do normalize vector."""

        tmpLen = physics.Physics.get_magnitude(self)

        if tmpLen > physics.Physics.EPSILON:
            invLen = 1.0 / tmpLen
            self.x *= invLen
            self.y *= invLen

    def rotate(self, rad):
        """Do rotate point.
        @param rad: Radians
        """
        c = math.cos(rad)
        s = math.sin(rad)

        xp = self.x * c - self.y * s
        yp = self.x * s + self.y * c

        self.x = xp
        self.y = yp

    def perpendicular(self):
        """Do perpendicular for this vector.
        """
        return Vector2(self.y, -self.x)

    def len_sqr(self):
        """Sum of of both square vectors."""
        return self.x * self.x + self.y * self.y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.get_x(), self.y + other.get_y())
        else:
            return Vector2(self.x + other, self.y + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.get_x(), self.y - other.get_y())
        else:
            return Vector2(self.x - other, self.y - other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.get_x(), self.y * other.get_y())
        else:
            return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.get_x(), self.y / other.get_y())
        else:
            return Vector2(self.x / other, self.y / other)

    def __rdiv__(self, other):
        return self.__div__(other)

    # --------------------------------------------
    # Protected Methods
    # --------------------------------------------

    # --------------------------------------------
    # Private Methods
    # --------------------------------------------

    # --------------------------------------------
    # setter / getter
    # --------------------------------------------
    def set_xy(self, newX, newY):
        self.x = newX
        self.y = newY

    def set_x(self, newX):
        self.x = newX

    def get_x(self):
        return self.x

    def set_y(self, newY):
        self.y = newY

    def get_y(self):
        return self.y
