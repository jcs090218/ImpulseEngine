# ========================================================================
# $File: shape.py $
# $Date: 2017-08-11 17:13:39 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

from jcspygm_physics.enum.shape_type import ShapeType
from jcspygm.core.JCSPyGm_GameObject import JCSPyGm_GameObject


class Shape(JCSPyGm_GameObject):
    """
    @class Shape
    @brief Shape base class. Inherit to 'JCSPyGm_GameObject' just
    to use the render layer.
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
    def __init__(self):
        """Constructor."""

        self.rigidbody = None

        self.color = (255, 255, 255)

        self.type = ShapeType.NONE

        self.thickness = 1

        self.initialize()

    #====================
    # Public Methods
    def initialize(self):
        """Initialize object depends on shape.

        IMPORTANT: override this...
        """

    def compute_mass(self, density):
        """Compute the mass by density.

        IMPORTANT: override this...
        """

    def set_orientation(self, radians):
        """Set the shape orientation by radians.

        IMPORTANT: override this...
        """

    #====================
    # Protected Methods

    #====================
    # Private Methods

    #====================
    # setter / getter
    def get_shape_type(self):
        """Return the enum type of shape."""
        return self.type

    def get_rigidbody(self):
        return self.rigidbody

    def get_position(self):
        return self.rigidbody.get_position()

    def get_x(self):
        return self.get_rigidbody().get_position().get_x()

    def get_y(self):
        return self.get_rigidbody().get_position().get_y()
