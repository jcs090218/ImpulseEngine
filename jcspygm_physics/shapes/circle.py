# ========================================================================
# $File: circle.py $
# $Date: 2017-08-11 16:57:09 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

from jcspygm.util.JCSPyGm_Debug import JCSPyGm_Debug
from jcspygm_physics.enum.shape_type import ShapeType
from jcspygm_physics.shape import Shape
from jcspygm_physics.rigidbody import Rigidbody

from jcspygm_physics.vector2 import Vector2

import jcspygm_physics.jcs_math
import math
import pygame

class Circle(Shape):
    """
    @class Circle
    @brief Circle shape object.
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
    def __init__(self, x, y, radius, density = 1.0):
        """Constructor."""

        super(Circle, self).__init__()

        self.radius = radius
        self.type = ShapeType.CIRCLE

        # override rigidbody
        self.rigidbody = Rigidbody(self, x, y)

        self.density = density
        self.compute_mass(self.density)

    #====================
    # Public Methods
    def update(self, deltaTime):
        """Update shape game logic"""

        # Do nothing if the body is not avaliable.
        if self.rigidbody is None:
            JCSPyGm_Debug.Log("There is shape without rigidbody in the scene...")
            return

    def draw(self, windowInfo):
        """Start render."""

        # Do nothing if the body is not avaliable.
        if self.rigidbody is None:
            JCSPyGm_Debug.Log("There is shape without rigidbody in the scene...")
            return

        # Render circle.

        draw_pos_x = int(self.rigidbody.get_position().get_x())
        draw_pos_y = int(self.rigidbody.get_position().get_y())

        pygame.draw.circle(
            windowInfo,
            self.color,
            (draw_pos_x, draw_pos_y),
            self.radius,
            self.thickness)

        # Render line within circle so orientation is visible
        line_vertices = []

        r = Vector2(0.0, 1.0)
        c = math.cos(self.rigidbody.get_orientation())
        s = math.sin(self.rigidbody.get_orientation())
        r.set_xy(r.x * c - r.y * s, r.x * s + r.y * c)
        r *= self.radius
        r += self.rigidbody.get_position()

        line_vertices.append((draw_pos_x, draw_pos_y))
        line_vertices.append((r.x, r.y))

        pygame.draw.lines(
            windowInfo,
            self.color,
            False,
            line_vertices)

    def compute_mass(self, density):
        """Compute the mass by density."""
        self.rigidbody.set_mass(jcspygm_physics.jcs_math.PI * self.radius * self.radius * density)
        self.rigidbody.set_inertia(self.rigidbody.get_mass() * self.radius * self.radius)

    def set_orientation(self, radians):
        """Set the shape orientation by radians."""
        # Every shape have to override this...

    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def get_radius(self):
        return self.radius
