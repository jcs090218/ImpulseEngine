# ========================================================================
# $File: manifold.py $
# $Date: 2017-08-11 16:37:12 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

from jcspygm.util.JCSPyGm_Debug import JCSPyGm_Debug
from jcspygm_physics.vector2 import Vector2
from jcspygm_physics.enum.shape_type import ShapeType

from jcspygm_physics.physics import Physics
from jcspygm_physics.collision import Collision

import jcs_math
import math

class Manifold(object):
    """
    @class Manifold
    @brief Here manifold refer as small objet that contains
    information about a collision between two objects.
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
    def __init__(self, shapeA, shapeB):
        """Constructor."""

        self.shapeA = shapeA
        self.shapeB = shapeB

        self.bodyA = self.shapeA.get_rigidbody()
        self.bodyB = self.shapeB.get_rigidbody()

        # depth of penetration from collision
        self.penetration = 0

        # normal from 'shapeA' to 'shapeB'
        self.normal = Vector2()

        # Points of contact during collision.
        self.contacts = []
        # only need two of them.
        self.contacts.append(Vector2())
        self.contacts.append(Vector2())

        # Number of contacts that occured during collision
        self.contact_count = 0

        self.mixed_restitution = 0
        self.mixed_dynamic_friction = 0
        self.mixed_static_friction = 0

    #====================
    # Public Methods
    def initialize(self, deltaTime):
        # Calculate average restitution
        self.mixed_restitution = min(
            self.bodyA.get_restitution(),
            self.bodyB.get_restitution())

        # Calculate static and dynamic friction
        self.mixed_static_friction = math.sqrt(
            self.bodyA.get_static_friction() *
            self.bodyA.get_static_friction())
        self.mixed_dynamic_friction = math.sqrt(
            self.bodyA.get_dynamic_friction() *
            self.bodyA.get_dynamic_friction())

        for index in range(0, self.contact_count):
            # Calculate radii from COM to contact
            ra = self.contacts[index] - self.bodyA.get_position()
            rb = self.contacts[index] - self.bodyB.get_position()

            rv = (self.bodyB.get_velocity() + jcs_math.cross_product_fv(self.bodyB.get_angular_velocity(), rb) -
                  self.bodyA.get_velocity() - jcs_math.cross_product_fv(self.bodyA.get_angular_velocity(), ra))

            # Determine if we should perform a resting collision
            # or not. The idea is if the only thing moving this
            # object is gravity, then the collision should be
            # performed without any restitution
            if rv.len_sqr() < (deltaTime * Physics.GRAVITY).len_sqr() + Physics.EPSILON:
                self.mixed_restitution = 0.0

    def solve(self):
        """Generate contact information."""

        shapeTypeA = self.shapeA.get_shape_type()
        shapeTypeB = self.shapeB.get_shape_type()

        # do nothing if type does not defined.
        if (shapeTypeA is ShapeType.NONE or
            shapeTypeB is ShapeType.NONE):
            JCSPyGm_Debug.Log("Type does not defined when trying to solve...")
            return

        if (shapeTypeA is ShapeType.CIRCLE and
            shapeTypeB is ShapeType.CIRCLE):
            Collision.circle_to_circle(self, self.shapeA, self.shapeB)
        elif (shapeTypeA is ShapeType.POLYGON and
              shapeTypeB is ShapeType.POLYGON):
            Collision.polygon_to_polygon(self, self.shapeA, self.shapeB)
        elif (shapeTypeA is ShapeType.CIRCLE and
              shapeTypeB is ShapeType.POLYGON):
            Collision.circle_to_polygon(self, self.shapeA, self.shapeB)
        elif (shapeTypeA is ShapeType.POLYGON and
              shapeTypeB is ShapeType.CIRCLE):
            Collision.polygon_to_circle(self, self.shapeA, self.shapeB)

    def apply_impulse(self):
        """Solve impulse and apply to it."""

        sum_inverse_mass = self.bodyA.get_inverse_mass() + self.bodyB.get_inverse_mass()

        if jcs_math.safe_equal(sum_inverse_mass, 0.0) is False:
            self.infinite_mass_correction()
            return

        for index in range(0, self.contact_count):
            # Calculate radii from COM to contact
            ra = self.contacts[index] - self.bodyA.get_position()
            rb = self.contacts[index] - self.bodyB.get_position()

            # Relative velocity
            rv = (self.bodyB.get_velocity() +
                  jcs_math.cross_product_fv(
                      self.bodyB.get_angular_velocity(), rb) -
                  self.bodyA.get_velocity() -
                  jcs_math.cross_product_fv(
                      self.bodyA.get_angular_velocity(), ra))

            # Relative velocity along the normal
            contact_vel = jcs_math.dot_product(rv, self.normal)

            # No need to resolve if velocitie are separating
            if contact_vel > 0:
                return

            ra_cross_n = jcs_math.cross_product(ra, self.normal)
            rb_cross_n = jcs_math.cross_product(rb, self.normal)
            inv_mass_sum = (self.bodyA.get_inverse_mass() +
                            self.bodyB.get_inverse_mass() +
                            (ra_cross_n * ra_cross_n) *
                            self.bodyA.get_inverse_inertia() +
                            (rb_cross_n * rb_cross_n) *
                            self.bodyB.get_inverse_inertia())

            # Calculate impulse scalar
            j = -(1.0 + self.mixed_restitution) * contact_vel
            j /= inv_mass_sum
            j /= float(self.contact_count)

            # Apply impulse
            impulse = self.normal * j
            self.bodyA.apply_impulse(-impulse, ra)
            self.bodyB.apply_impulse(impulse, rb)

            # Friction impulse
            rv = (self.bodyB.get_velocity() +
                  jcs_math.cross_product_fv(
                      self.bodyB.get_angular_velocity(), rb) -
                  self.bodyA.get_velocity() -
                  jcs_math.cross_product_fv(
                      self.bodyA.get_angular_velocity(), ra))

            t = rv - (self.normal * jcs_math.dot_product(rv, self.normal))
            t.normalize()

            # j tangent magnitude
            jt = -jcs_math.dot_product(rv, t)
            jt /= inv_mass_sum
            jt /= self.contact_count

            # Do not apply tiny friction impulses
            if jcs_math.safe_equal(jt, 0.0):
                return

            # Coulumb's law
            tangentImpulse = Vector2()
            if jcs_math.absolute_value(jt) < j * self.mixed_static_friction :
                tangentImpulse = t * jt
            else:
                tangentImpulse = t * -j * self.mixed_dynamic_friction

            # Apply friction impulse
            self.bodyA.apply_impulse(-tangentImpulse, ra)
            self.bodyB.apply_impulse(tangentImpulse, rb)

    def positional_correction(self):
        """Naive correction of positional penetration."""
        slop = 0.05
        percent = 0.4

        # NOTE(jenchieh): This return 'Vector2' because of
        # 'self.normal' is type of Vector2
        correction = (
            max(self.penetration - slop, 0.0) /
            (self.bodyA.get_inverse_mass() +
             self.bodyB.get_inverse_mass())
                      * self.normal
                      * percent)

        self.bodyA.position -= correction * self.bodyA.get_inverse_mass()
        self.bodyB.position += correction * self.bodyB.get_inverse_mass()

    def infinite_mass_correction(self):
        """Set both shape's velocity to zero."""
        shapeA_vel = self.shapeA.get_rigidbody().get_velocity()
        shapeA_vel.set_x(0)
        shapeA_vel.set_y(0)

        shapeB_vel = self.shapeB.get_rigidbody().get_velocity()
        shapeB_vel.set_x(0)
        shapeB_vel.set_y(0)

    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def set_normal(self, val):
        """ @param{ Vector2 } val : vector normal. """
        self.normal = val

    def get_normal(self):
        """ @return { Vector2 } : vector 2 real number. """
        return self.normal

    def set_penetration(self, val):
        """ @param{ float } val : penetration real number """
        self.penetration = val

    def get_penetration(self):
        """ @return { float } : current penetration real number. """
        return self.penetration

    def set_contact_count(self, newCount):
        """ @param { int } newCount : value to update contact count. """
        self.contact_count = newCount

    def get_contact_count(self):
        """ @return { int } : current contact count. """
        return self.contact_count

    def set_contacts_at(self, index, newContact):
        """ @param { int } index : set the contact at index.
            @param { Vector2 } newContact : new contact info. """
        self.contacts[index] = newContact

    def get_contacts_at(self, index):
        """ @return { Vector2 } """
        return self.contacts[index]
