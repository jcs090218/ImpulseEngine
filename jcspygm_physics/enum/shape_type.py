# ========================================================================
# $File: shape_type.py $
# $Date: 2017-08-12 13:13:51 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright (c) 2017 by Shen, Jen-Chieh $
# ========================================================================

class ShapeType(object):
    """
    @enum ShapeType
    @brief List of all the shape.
    @note Remember to install 'aenum' and 'enum34' from pip.
    """
    NONE, CIRCLE, POLYGON = range(3)
