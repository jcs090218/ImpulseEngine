#  ========================================================================
#  $File: physics.py $
#  $Date: 2017-01-16 03:38:53 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================

import jcs_math
import vector2


class Physics(object):

    """All physic relate function will be put in this file."""

    # --------------------------------------------
    # Public Variables
    # --------------------------------------------
    GRAVITY_SCALE = 15.0
    GRAVITY = vector2.Vector2(0, 9.81 * GRAVITY_SCALE)
    EPSILON = 0.0001

    # --------------------------------------------
    # Private Variables
    # --------------------------------------------

    # --------------------------------------------
    # Protected Variables
    # --------------------------------------------

    # --------------------------------------------
    # Constructor
    # --------------------------------------------

    # --------------------------------------------
    # Public Methods
    # --------------------------------------------
    @staticmethod
    def unit_vector(vec2):
        """Return the unit vector base on two point.

        @param vec2: Vector2 you want to target.
        """
        tmpLen = Physics.get_mgnitude(vec2)

        if tmpLen > Physics.EPSILON:
            invLen = 1.0 / tmpLen
            vec2.x *= invLen
            vec2.y *= invLen

    @staticmethod
    def get_magnitude(vec2):
        """Return magnitude base on two coordinate.

        @param vec2: Vector2 you want to target.
        @return magnitude / absolute value of vector length
        """
        return jcs_math.pythagorean_theorem(vec2.x, vec2.y, "hyp")

    @staticmethod
    def get_normalize(vec2):
        """Modified normalize value.

        @param vec2: Vector2 you want to target.
        """
        Physics.unit_vector(vec2)

    @staticmethod
    def get_perpendicular(vec2):
        """Return perpendicular value.

        @param vec2: Vector2 you want to target.
        @return perpendicular value.
        """
        return vector2.Vector2(vec2.y, -vec2.x)

    @staticmethod
    def point_distance(pointA, pointB):
        """Return the distance between two points.

        @param { Vector2 } pointA : first point.
        @param { Vector2 } pointB : second point.
        @return { float } : distance between two points.
        """

        vDistance = jcs_math.absolute_value(pointA.get_y() - pointB.get_y())
        hDistance = jcs_math.absolute_value(pointA.get_x() - pointB.get_x())

        return jcs_math.pythagorean_theorem(vDistance, hDistance, "hyp")

    @staticmethod
    def dist_sqr(vecA, vecB):
        """Distance angle.
        @param { Vector2 } vecA : vector A.
        @param { Vector2 } vecB : vector B.
        @return { float } : angle value.
        """
        vecC = vecA - vecB
        return jcs_math.dot_product(vecC, vecC)

    @staticmethod
    def integrate_forces(shape, deltaTime):
        """SEE: http://www.niksula.hut.fi/~hkankaan/Homepages/gravity.html"""

        tmpBody = shape.get_rigidbody()

        if tmpBody.get_inverse_mass() == 0.0:
            return

        halfDeltaTime = deltaTime * 0.5

        tmpBody.velocity += (tmpBody.get_force() * tmpBody.get_inverse_mass() + Physics.GRAVITY) * halfDeltaTime
        tmpBody.angular_velocity += tmpBody.torque * tmpBody.get_inverse_inertia() * halfDeltaTime

    @staticmethod
    def integrate_velocity(shape, deltaTime):
        """Start the velocity in physics world."""
        tmpBody = shape.get_rigidbody()

        if tmpBody.get_inverse_mass() == 0.0:
            return

        tmpBody.position += tmpBody.velocity * deltaTime
        # STUDY(jenchieh): angular_velocity is too small
        # and cannot be add up.
        tmpBody.orientation += (tmpBody.angular_velocity * deltaTime)

        tmpBody.set_orientation(tmpBody.orientation)
        Physics.integrate_forces(shape, deltaTime)


    # --------------------------------------------
    # Protected Methods
    # --------------------------------------------

    # --------------------------------------------
    # Private Methods
    # --------------------------------------------

    # --------------------------------------------
    # setter / getter
    # --------------------------------------------
