#  ========================================================================
#  $File: math.py $
#  $Date: 2017-01-15 23:14:10 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================

from jcspygm.util.JCSPyGm_Debug import JCSPyGm_Debug
import math

import physics
import vector2


PI = 3.141592741
FLT_MAX = 3.4028235e38

def absolute_value(val):
    """Return the absolute value.
    @return val: value to assign as absolute value.
    """
    return val if val < 0 else -val;
2
def to_positive(val):
    """Make the value to positive. (so as the same as absolute value)
    @return val: convert to positive value.
    """
    return absolute_value(val)

def to_negative(val):
    """Make the value to negative.
    @return val: convert to negative value.
    """
    return -absolute_value(val)

def pythagorean_theorem(side1, side2, targetSide):
    """Do pythagorean theorem
    @param side1: side a
    @param side2: side b
    @param targetSide: side we want to find. (opp, adj, hyp)
    @return pythagorean theorom result by the type entered.
    """

    result = 0

    # target either opposite or adjacent
    if targetSide is "adj" or targetSide is "opp":

        # distinct the side base on the side length.
        oppOrAdj = min(side1, side2)
        hyp = max(side1, side2)

        result = math.sqrt(sqr(hyp) - sqr(oppOrAdj))

    # targeting hypotenuse
    elif targetSide is "hyp":
        # hypotenuse just simple addition.
        result = math.sqrt(sqr(side1) + sqr(side2))
    else:
        JCSPyGm_Debug.Error(
            "Type enter does not exist. "
            + "Please enter either opp/adj/hyp.");

    return result

def dot_product(vec1, vec2):
    """Do dot product with two vector.
    @param { Vector2 } vec1 : first vector.
    @param { Vector2 } vec2 : second vector.
    @return { float } : dot product result.
    """

    return vec1.get_x() * vec2.get_x() + vec1.get_y() * vec2.get_y()

def cross_product(vec1, vec2):
    """
    Do cross product with two vector.
    @param { Vector2 } vec1 : first vector.
    @param { Vector2 } vec2 : second vector.
    @return { float } : Return the scalar.
    """

    return vec1.get_x() * vec2.get_y() - vec1.get_y() * vec2.get_x()

def cross_product_fv(val, vec):
    """
    Do cross product with one vector and one real number.
    @param { float } val : real number.
    @param { Vector2 } vec : vector2.
    @return { Vector2 } : return cross product result.
    """

    return vector2.Vector2(-val * vec.get_y(), val * vec.get_x())

def cross_product_vf(vec, val):
    """
    Do cross product with one vector and one real number.
    @param { Vector2 } vec : vector2.
    @param { float } val : real number.
    @return { Vector2 } : return cross product result.
    """

    return vector2.Vector2(val * vec.get_y(), -val * vec.get_x())

def sqr(val):
    """Square the value.
    @param val: value to be square
    @return result.
    """

    return val * val

def safe_equal(valA, valB):
    """
    Comparison with tolerance of EPSILON
    """

    return absolute_value(valA - valB) <= physics.Physics.EPSILON

def bias_greater_than(a, b):
    """
    """

    bias_relative = 0.95
    bias_absolute = 0.01
    return a >= b * bias_relative + a * bias_absolute
