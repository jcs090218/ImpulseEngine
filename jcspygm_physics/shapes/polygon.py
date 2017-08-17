# ========================================================================
# $File: polygon.py $
# $Date: 2017-08-11 17:17:59 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

from jcspygm.util.JCSPyGm_Debug import JCSPyGm_Debug
from jcspygm_physics.enum.shape_type import ShapeType
from jcspygm_physics.shape import Shape

from jcspygm_physics.rigidbody import Rigidbody
from jcspygm_physics.mat2 import Mat2
from  jcspygm_physics.vector2 import Vector2
from jcspygm_physics.physics import Physics
import jcspygm_physics.jcs_math

import pygame

class Polygon(Shape):
    """
    @class Polygon
    @brief Polygon shape class.
    """

    #*********************************************#
    #*             Public Variables              *#
    #*********************************************#
    MAX_POLY_VERTEX_COUNT = 64

    #*********************************************#
    #              Private Variables             *#
    #*********************************************#

    #*********************************************#
    #              Protected Variables           *#
    #*********************************************#

    #*********************************************#
    #                Constructor                 *#
    #*********************************************#
    def __init__(self, x, y, density = 1):
        """
        Constructor.
        @param { Vector2 } x : position on x-axis.
        @param { Vector2 } y : position on y-axis.
        @param { float } density : density use to calculate mass.
        """

        super(Polygon, self).__init__()

        self.type = ShapeType.POLYGON

        # override rigidbody
        self.rigidbody = Rigidbody(self, x, y)

        # Orientation matrix from model to world
        self.orientation = Mat2()

        # { Vector2[] } : List of vertices.
        self.vertices = []
        self.vertex_count = 0
        self.normals = []

        # Initialize the two vector2's array.
        for count in range(0, Polygon.MAX_POLY_VERTEX_COUNT):
            self.vertices.append(Vector2())
            self.normals.append(Vector2())

        self.density = density

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

        draw_vertices = []

        for index in range(0, self.vertex_count):
            tmpVec = (self.rigidbody.get_position() +
                      self.orientation *
                      self.vertices[index])
            tmpPoint = (tmpVec.get_x(), tmpVec.get_y())

            # add to vertices list.
            draw_vertices.append(tmpPoint)

        pygame.draw.polygon(
            windowInfo,
            self.color,
            draw_vertices,
            self.thickness)

    def compute_mass(self, density):
        """Compute the mass by density."""

        # Calculate centroid and moment of interia
        centroid = Vector2(0.0, 0.0)
        area = 0.0
        I = 0.0
        inv3 = 1.0 / 3.0

        for count in range(0, self.vertex_count):

            # Triangle vertices, third vertex implied as (0, 0)
            p1 = self.vertices[count]
            p2 = self.vertices[(count + 1) % self.vertex_count]

            d = jcspygm_physics.jcs_math.cross_product(p1, p2)
            triangle_area = 0.5 * d

            area += triangle_area

            # Use area to weight the centroid average, not
            # just vertex position
            weight = triangle_area * inv3 * (p1 + p2)
            centroid += weight

            intx2 = p1.x * p1.x + p2.x * p1.x + p2.x * p2.x
            inty2 = p1.y * p1.y + p2.y * p1.y + p2.y * p2.y

            I += (0.25 * inv3 * d) * (intx2 + inty2)

        # check area.
        if area == 0:
            JCSPyGm_Debug.Log("Polygon shape's area is zero???")
            return

        centroid *= 1.0 / area

        # Translate vertices to centroid (make the centroid (0, 0)
        # for the polygon in model space)
        # Not really necessary, but I like doing this anyway
        for index in range(0, self.vertex_count):
            self.vertices[index] -= centroid

        self.rigidbody.set_mass(density * area)
        self.rigidbody.set_inertia(I * density)


    def set_orientation(self, radians):
        """Set the shape orientation by radians."""
        self.orientation.set_mat_by_radians(radians)

    def set_box(self, half_width, half_height):
        """Set polygon to perfect box shape."""

        self.vertex_count = 4

        self.vertices[0].set_xy(-half_width, -half_height)
        self.vertices[1].set_xy(half_width, -half_height)
        self.vertices[2].set_xy(half_width, half_height)
        self.vertices[3].set_xy(-half_width, half_height)
        self.normals[0].set_xy(0.0, -1.0)
        self.normals[1].set_xy(1.0, 0.0)
        self.normals[2].set_xy(0.0, 1.0)
        self.normals[3].set_xy(-1.0, 0.0)

        self.compute_mass(self.density)

    def set_rand_convex_poly(self, vertices, count):
        """
        Generate the random convex polygon shape.
        @param { Vector2[] } vertices: list of vertices.
        @param { int } count : count.
        """

        # No hulls with less than 3 vertices (ensure actual polygon)
        if (count > 2 and count <= Polygon.MAX_POLY_VERTEX_COUNT) is False:
            JCSPyGm_Debug.Error("No hulls with less than 3 vertices (ensure actual polygon).")

        count = min(count, Polygon.MAX_POLY_VERTEX_COUNT)

        # Find the right most point on the hull
        right_most = 0
        highest_x_coord = vertices[0].get_x()

        for index in range(1, count):
            x = vertices[index].get_x()

            if x > highest_x_coord:
                highest_x_coord = x
                right_most = index

            # If matching x then take farthest negative y
            elif x == highest_x_coord:
                if vertices[index].y < vertices[right_most].y:
                    right_most = index


        # 'Integer' array.
        hull = []
        for index in range(0, Polygon.MAX_POLY_VERTEX_COUNT):
            hull.append(0)
        out_count = 0
        index_hull = right_most

        while True:
            hull[out_count] = index_hull

            # Search for next index that wraps around the hull
            # by computing cross products to find the most counter-clockwise
            # vertex in the set, given the previos hull index
            next_hull_index = 0
            for index in range(1, count):
                if next_hull_index == index_hull:
                    next_hull_index = index
                    continue

                # Cross every set of three unique vertices
                # Record each counter clockwise third vertex and add
                # to the output hull
                # SEE: http://www.oocities.org/pcgpe/math2d.html
                e1 = vertices[next_hull_index] - vertices[hull[out_count]]
                e2 = vertices[index] - vertices[hull[out_count]]
                c = jcspygm_physics.jcs_math.cross_product(e1, e2)
                if c < 0.0:
                    next_hull_index = index

                # Cross product is zero then e vectors are
                # on same line therefor want to record vertex
                # farthest along that line
                if (c == 0.0 and
                    e2.len_sqr() > e1.len_sqr()):
                    next_hull_index = index

            out_count += 1
            index_hull = next_hull_index

            # Conclude algorithm upon wrap-around
            if next_hull_index == right_most:
                self.vertex_count = out_count
                break

        # Copy vertices into shape's vertices
        for index in range(0, self.vertex_count):
            self.vertices[index] = vertices[hull[index]]

        # Compute face normals
        for index in range(0, self.vertex_count):
            if index + 1 < self.vertex_count:
                index2 = index + 1
            else:
                index2 = 0
            face = self.vertices[index2] - self.vertices[index]

            # Ensure no zero-length edges, because that's bad
            if (face.len_sqr() > Physics.EPSILON * Physics.EPSILON) is False:
                JCSPyGm_Debug.Error("Ensure no zero-length edges, because that's bad...")

            # Calculate normal with 2D cross product
            # between vector and scalar
            self.normals[index] = Vector2(face.y, -face.x)
            self.normals[index].normalize()

        # set the mass.
        self.compute_mass(self.density)

    def get_support(self, in_direction):
        """
        The extreme point along a direction within a polygon.
        @param { Vector2 } in_direction : vector direction.
        @return { Vector2 } : The extreme point along a direction
        within a polygon.
        """

        best_projection = -3.4028235e38
        best_vertex = Vector2()

        for index in range(0, self.vertex_count):
            v = self.vertices[index]
            projection = jcspygm_physics.jcs_math.dot_product(v, in_direction)
            
            if projection > best_projection:
                best_vertex = v
                best_projection = projection

        return best_vertex


    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def get_vertex_count(self):
        return self.vertex_count
