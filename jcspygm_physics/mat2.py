# ========================================================================
# $File: mat2.py $
# $Date: 2017-08-14 06:37:13 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

import math
import jcs_math

import vector2

class Mat2(object):

    """
    @class Mat2
    @brief Matrix world position in order to identify the
    polygon orientation.
    """

    #*********************************************#
    #*             Public Variables              *#
    #*********************************************#

    #*********************************************#
    #              Private Variables             *#
    #*********************************************#

    #*********************************************#
    #              Protected Variables           *#
    #*********************************************#

    #*********************************************#
    #                Constructor                 *#
    #*********************************************#
    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        """Constructor."""

        self.m00 = a
        self.m01 = b
        self.m10 = c
        self.m11 = d

    #====================
    # Public Methods
    def abs_mat(self, inMat):
        """Set absolute all matrix and return new one."""

        inMat.m00 = jcs_math.absolute_value(self.m00)
        inMat.m01 = jcs_math.absolute_value(self.m01)
        inMat.m10 = jcs_math.absolute_value(self.m10)
        inMat.m11 = jcs_math.absolute_value(self.m11)
        return inMat

    def get_axis_x(self, inVec):
        """Sets out to the x-axis (1st column) of this matrix."""
        inVec.set_x(self.m00)
        inVec.set_y(self.m10)
        return inVec

    def get_axis_y(self, inVec):
        """Sets out to the y-axis (2nd column) of this matrix."""
        inVec.set_x(self.m01)
        inVec.set_y(self.m11)
        return inVec

    def transposei(self):
        t = self.m01
        self.m01 = self.m10
        self.m10 = t

    def transpose(self):
        """
        Transpose the current matrix.
        @return { Mat2 } : return a transpose matrix object.
        """
        return Mat2(self.m00, self.m10, self.m01, self.m11)

    def __mul__(self, other):
        if isinstance(other, vector2.Vector2):
            return vector2.Vector2(
                self.m00 * other.get_x() + self.m01 * other.get_y(),
                self.m10 * other.get_x() + self.m11 * other.get_y())

    def __rmul__(self, other):
        return self.__mul__(other)

    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def set_mat_by_radians(self, radians):
        """Set mat2 by calculate the radians."""
        c = math.cos(radians)
        s = math.sin(radians)

        self.m00 = c
        self.m01 = -s
        self.m10 = s
        self.m11 = c

    def set_mat_by_mat(self, newMat):
        """Set mat2 by another mat2."""
        self.m00 = newMat.m00
        self.m01 = newMat.m01
        self.m10 = newMat.m10
        self.m11 = newMat.m11

    def set_mat_by_val(self, a, b, c, d):
        """Set mat2 by each individual value."""
        self.m00 = a
        self.m01 = b
        self.m10 = c
        self.m11 = d
