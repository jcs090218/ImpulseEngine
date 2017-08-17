#  ========================================================================
#  $File: collision.py $
#  $Date: 2017-02-01 06:47:15 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================

import jcs_math

import vector2

import math
import sys

from jcspygm_physics.physics import Physics
from jcspygm_physics.vector2 import Vector2


class Collision(object):
    """
    @class Collision
    @brief List of all the collision type here...
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

    # --------------------------------------------
    # Public Methods
    # --------------------------------------------
    @staticmethod
    def circle_to_circle(manifold, circA, circB):
        """Do collision check on two circle.

        @param { Manifold } manifold : information about a
        collision between two objects.
        @param { Circle } circA : Circle Shape A with rigidbody.
        @param { Circle } circB : Circle Shape B with rigidbody.
        """

        # Calculate translational vector, which is normal
        normal = circB.get_position() - circA.get_position()

        dist_sqr = normal.len_sqr()
        radius = circA.get_radius() + circB.get_radius()

        # Not in contact
        if dist_sqr >= jcs_math.sqr(radius):
            manifold.set_contact_count(0)
            return

        distance = math.sqrt(dist_sqr)

        manifold.set_contact_count(1)

        if distance == 0:
            manifold.set_penetration(circA.get_radius())
            manifold.set_normal(vector2.Vector2(1, 0))
            manifold.set_contacts_at(0, circA.get_position())
        else:
            manifold.set_penetration(radius - distance)
            # aster than using Normalized since we already
            # performed sqrt
            manifold.set_normal(normal / distance)

            tmpContact = manifold.get_normal() * circA.get_radius() + circA.get_position()
            manifold.set_contacts_at(0, tmpContact)

    @staticmethod
    def circle_to_polygon(manifold, circ, poly):
        """Do collision check with polygon and circle.

        @param { Manifold } manifold : information about a
        collision between two objects.
        @param { Circle } circ: Circle to check collide with Polygon.
        @param { Polygon } poly: Polygon to check collide with circle.
        """

        circBody = circ.get_rigidbody()
        polyBody = poly.get_rigidbody()

        manifold.contact_count = 0

        # Transform circle center to Polygon model space
        center = (poly.orientation.transpose() *
                  (circBody.get_position() - polyBody.get_position()))

        # Find edge with minimum penetration
        # Exact concept as using support points in Polygon vs Polygon
        separation = -jcs_math.FLT_MAX
        face_normal = 0

        for index in range(0, poly.get_vertex_count()):
            s = jcs_math.dot_product(poly.normals[index], center - poly.vertices[index])

            if s > circ.get_radius():
                return

            if s > separation:
                separation = s
                face_normal = index

        # Grab face's vertices
        v1 = poly.vertices[face_normal]
        if face_normal + 1 < poly.get_vertex_count():
            i2 = face_normal + 1
        else:
            i2 = 0
        v2 = poly.vertices[i2]

        # Check to see if center is within polygon
        if separation < Physics.EPSILON:
            manifold.contact_count = 1
            manifold.normal = -(poly.orientation * poly.normals[face_normal])
            manifold.contacts[0] = manifold.normal * circ.get_radius() + circBody.get_position()
            manifold.penetration = circ.get_radius()
            return

        dot1 = jcs_math.dot_product(center - v1, v2 - v1)
        dot2 = jcs_math.dot_product(center - v2, v1 - v2)
        manifold.penetration = circ.get_radius() - separation

        # Close to v1
        if dot1 <= 0.0:
            if Physics.dist_sqr(center, v1) > circ.get_radius() * circ.get_radius():
                return

            manifold.contact_count = 1
            n = poly.orientation * (v1 - center)
            n.normalize()
            manifold.normal = n
            v1 = poly.orientation * v1 + polyBody.get_position()
            manifold.contacts[0] = v1

        # Close to v2
        elif dot2 <= 0.0:
            if Physics.dist_sqr(center, v2) > circ.get_radius() * circ.get_radius():
                return

            manifold.contact_count = 1
            v2 = poly.orientation * v2 + polyBody.get_position()
            manifold.contacts[0] = v2

            n = poly.orientation * (v2 - center)
            n.normalize()
            manifold.normal = n

        # Closest to face
        else:
            n = poly.normals[face_normal]
            if jcs_math.dot_product(center - v1, n) > circ.get_radius():
                return

            n = poly.orientation * n
            manifold.normal = -n
            manifold.contacts[0] = manifold.normal * circ.get_radius() + circBody.get_position()
            manifold.contact_count = 1

    @staticmethod
    def polygon_to_circle(manifold, poly, circ):
        """Do collision check with polygon and circle.

        @param { Manifold } manifold : information about a
        collision between two objects.
        @param { Polygon } poly: Polygon to check collide with circle.
        @param { Circle } circ: Circle to check collide with Polygon.
        """
        Collision.circle_to_polygon(manifold, circ, poly)
        manifold.normal = -manifold.normal

    @staticmethod
    def polygon_to_polygon(manifold, polyA, polyB):
        """Do collision check with two polygon

        @param { Manifold } manifold : information about a
        collision between two objects.
        @param { Polygon } polyA: Polygon A to check collide with polygon B.
        @param { Polygon } polyB: Polygon B to check collide with polygon A.
        """

        bodyA = polyA.get_rigidbody()
        bodyB = polyB.get_rigidbody()

        manifold.contact_count = 0

        # Check for a separating axis with A's face planes

        penetrationA, faceA = Collision.find_axis_least_penetration(
            polyA, polyB)
        if penetrationA >= 0.0:
            return

        # Check for a separating axis with B's face planes
        penetrationB, faceB = Collision.find_axis_least_penetration(
            polyB, polyA)
        if penetrationB >= 0.0:
            return

        reference_index = 0
        flip = False  # Always point from a to b

        ref_poly = None  # Reference
        inc_poly = None  # Incident

        # Determine which shape contains reference face
        if jcs_math.bias_greater_than(penetrationA, penetrationB):
            ref_poly = polyA
            inc_poly = polyB
            reference_index = faceA
            flip = False
        else:
            ref_poly = polyB
            inc_poly = polyA
            reference_index = faceB
            flip = True

        # World space incident face
        incident_face = []
        for count in range(0, 2):
            incident_face.append(Vector2())
        Collision.find_incident_face(
            incident_face,
            ref_poly,
            inc_poly,
            reference_index)

        #        y
        #        ^  ->n       ^
        #      +---c ------posPlane--
        #  x < | i |\
        #      +---+ c-----negPlane--
        #             \       v
        #              r
        #
        #  r : reference face
        #  i : incident poly
        #  c : clipped point
        #  n : incident normal

        # Setup reference face vertices
        v1 = ref_poly.vertices[reference_index]

        if reference_index + 1 == ref_poly.vertex_count:
            reference_index = 0
        else:
            reference_index += 1

        v2 = ref_poly.vertices[reference_index]

        # Transform vertices to world space
        v1 = ref_poly.orientation * v1 + ref_poly.get_rigidbody().get_position()
        v2 = ref_poly.orientation * v2 + ref_poly.get_rigidbody().get_position()

        # Calculate reference face side normal in world space
        side_plane_normal = (v2 - v1)
        side_plane_normal.normalize()

        # Orthogonalize
        ref_face_normal = Vector2(side_plane_normal.y, -side_plane_normal.x)

        # ax + by = c
        # c is distance from origin
        refC = jcs_math.dot_product(ref_face_normal, v1)
        neg_side = -jcs_math.dot_product(side_plane_normal, v1)
        pos_side = jcs_math.dot_product(side_plane_normal, v2)

        # Clip incident face to reference face side planes
        if Collision.clip(-side_plane_normal, neg_side, incident_face) < 2:
            # Due to floating point error, possible to not have required points
            return;
        if Collision.clip(side_plane_normal, pos_side, incident_face) < 2:
            # Due to floating point error, possible to not have required points
            return;

        # Flip
        if flip is True:
            manifold.normal = -ref_face_normal
        else:
            manifold.normal = ref_face_normal

        # Keep points behind reference face
        cp = 0  # clipped points behind reference face
        separation = jcs_math.dot_product(ref_face_normal, incident_face[0]) - refC
        if separation <= 0.0:
            manifold.contacts[cp] = incident_face[0]
            manifold.penetration = -separation
            cp += 1
        else:
            manifold.penetration = 0

        separation = jcs_math.dot_product(ref_face_normal, incident_face[1]) - refC
        if separation <= 0.0:
            manifold.contacts[cp] = incident_face[1]
            manifold.penetration += -separation
            cp += 1

            # Average penetration
            manifold.penetration /= float(cp)

        manifold.contact_count = cp

    @staticmethod
    def find_axis_least_penetration(polyA, polyB):
        """
        Find axis the least penetration.

        @param { Polygon } polyA : polygon shape A.
        @param { Polygon } polyB : polygon shape B.
        @return { int } : greatest penetration index.
        """

        best_distance = -jcs_math.FLT_MAX
        best_index = 0

        for index in range(0, polyA.vertex_count):
            # Retrieve a face normal from A
            n = polyA.normals[index]
            nw = polyA.orientation * n

            # Transform face normal into B's model space
            buT = polyB.orientation.transpose()
            n = buT * nw

            # Retrieve support point from B along -n
            s = polyB.get_support(-n)

            # Retrieve vertex on face from A, transform into
            # B's model space
            v = polyA.orientation * polyA.vertices[index] + polyA.get_rigidbody().get_position()
            v -= polyB.get_rigidbody().get_position()
            v = buT * v

            # Compute penetration distance (in B's model space)
            d = jcs_math.dot_product(n, s - v)

            # Store greatest distance
            if d > best_distance:
                best_distance = d
                best_index = index

        return best_distance , best_index

    @staticmethod
    def clip(n, c, face):
        """Clip"""

        sp = 0
        out = [
            face[0],
            face[1]
        ]

        # Retrieve distances from each endpoint to the line
        # d = ax + by - c
        d1 = jcs_math.dot_product(n, face[0]) - c
        d2 = jcs_math.dot_product(n, face[1]) - c

        # If negative (behind plane) clip
        if d1 <= 0.0:
            out[sp] = face[0]
            sp += 1

        if d2 <= 0.0:
            out[sp] = face[1]
            sp += 1

        # If the points are on different sides of the plane
        if d1 * d2 < 0.0:  # less than to ignore -0.0f
            # Push interesction point
            alpha = d1 / (d1 - d2)
            out[sp] = face[0] + alpha * (face[1] - face[0])
            sp += 1

        # Assign our new converted values
        face[0] = out[0]
        face[1] = out[1]

        if (sp != 3) is False:
            JCSPyGm_Debug.Error("'sp' is equal to 3...")

        return sp

    @staticmethod
    def find_incident_face(v, ref_poly, inc_poly, reference_index):
        """
        Find incident face

        @param { Vector2[] } v : incident face list.
        @param { Polygon } ref_poly : reference polygon shape.
        @param { Polygon } inc_poly : incident polygon shape.
        """

        reference_normal = ref_poly.normals[reference_index]

        # Calculate normal in incident's frame of reference
        # To world space
        reference_normal = ref_poly.orientation * reference_normal
        # To incident's model space
        reference_normal = inc_poly.orientation.transpose() * reference_normal

        # Find most anti-normal face on incident polygon
        incident_face = 0
        min_dot = jcs_math.FLT_MAX

        for index in range(0, inc_poly.vertex_count):
            dot = jcs_math.dot_product(reference_normal, inc_poly.normals[index])
            if dot < min_dot:
                min_dot = dot
                incident_face = index

        # Assign face vertices for 'incident_face'
        v[0] = (inc_poly.orientation *
                inc_poly.vertices[incident_face] +
                inc_poly.get_rigidbody().get_position())

        if incident_face + 1 >= int(inc_poly.vertex_count):
            incident_face = 0
        else:
            incident_face += 1

        v[1] = (inc_poly.orientation *
                inc_poly.vertices[incident_face] +
                inc_poly.get_rigidbody().get_position())


    # --------------------------------------------
    # Protected Methods
    # --------------------------------------------

    # --------------------------------------------
    # Private Methods
    # --------------------------------------------

    # --------------------------------------------
    # setter / getter
    # --------------------------------------------
