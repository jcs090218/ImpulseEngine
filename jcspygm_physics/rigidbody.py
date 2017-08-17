# ========================================================================
# $File: rigidbody.py $
# $Date: 2017-08-11 16:27:16 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

from jcspygm_physics.vector2 import Vector2

import jcs_math

import math
import random


class Rigidbody(object):
    """Rigidbody base class."""

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
    def __init__(self, shape, x, y):
        """Constructor."""

        # record the shape.
        self.shape = shape

        # Linear components
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0

        # Angular components
        self.orientation = random.uniform(-jcs_math.PI, jcs_math.PI)
        self.angular_velocity = 0
        self.torque = 0

        # set by shape
        self.inertia = 0
        self.inverse_inertia = 0
        self.inverse_mass = 0
        self.mass = 0

        self.static_friction = 0.5
        self.dynamic_friction = 0.3
        self.restitution = 0.2

        self.force = Vector2(0, 0)

        self.is_static = False

    #====================
    # Public Methods
    def apply_force(self, force):
        """
        Apply force.
        @param { Vector2 } force : another vector force.
        """
        self.force += force

    def apply_impulse(self, impulse, contact_vec):
        """
        Apply Impulse
        @param { Vector2 } impulse : Impulse.
        @param { Vector2 } contact_vec : contact point.
        """
        self.velocity += self.inverse_mass * impulse
        self.angular_velocity += self.inverse_inertia * jcs_math.cross_product(contact_vec, impulse)

    def set_static(self):
        """Set the rigidbody static object in the world."""
        self.mass = 0
        self.inverse_mass = 0
        self.inertia = 0
        self.inverse_inertia = 0

        self.is_static = True

    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def set_orientation(self, radians):
        """Set orientation by passing in radians."""
        self.orientation = radians
        self.shape.set_orientation(radians)

    def get_orientation(self):
        return self.orientation

    def set_force(self, inForce):
        self.force = inForce

    def get_force(self):
        return self.force

    def set_mass(self, mass):
        """While setting the new mass, we need to recalculate the
        inverse mass.

        NOTE(jenchieh): When set mass 'inverse_mass'
        will be set automatically.
        """
        self.mass = mass

        if self.mass == 0:
            self.inverse_mass = 0
        else:
            self.inverse_mass = 1 / self.mass

    def get_mass(self):
        return self.mass

    def set_inverse_mass(self, newIM):
        self.inverse_mass = newIM

    def get_inverse_mass(self):
        return self.inverse_mass

    def set_angular_velocity(self, newAV):
        self.angular_velocity = newAV

    def get_angular_velocity(self):
        return self.angular_velocity

    def set_inertia(self, newI):
        """NOTE(jenchieh): When set mass 'inversr_inertia'
        will be set automatically.
        """
        self.inertia = newI

        if self.inertia == 0.0:
            self.inverse_inertia = 0.0
        else:
            self.inverse_inertia = 1.0 / self.inertia

    def get_inertia(self):
        return self.inertia

    def set_inverse_inertia(self, newII):
        self.inverse_inertia = newII

    def get_inverse_inertia(self):
        return self.inverse_inertia

    def set_restitution(self, newR):
        self.restitution = newR

    def get_restitution(self):
        return self.restitution

    def set_dynamic_friction(self, newDF):
        self.dynamic_friction = newDF

    def get_dynamic_friction(self):
        return self.dynamic_friction

    def set_static_friction(self, newSF):
        self.static_friction = newSF

    def get_static_friction(self):
        return self.static_friction
