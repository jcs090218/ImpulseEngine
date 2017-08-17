#  ========================================================================
#  $File: game.py $
#  $Date: 2017-01-16 01:55:11 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================

from jcspygm.core.JCSPyGm_Interface import JCSPyGm_Interface
from jcspygm.core.JCSPyGm_Scene import JCSPyGm_Scene
from jcspygm.managers.JCSPyGm_SceneManager import JCSPyGm_SceneManager
from jcspygm.util.JCSPyGm_Input import JCSPyGm_Input

from jcspygm_physics.physics import Physics
from jcspygm_physics.vector2  import Vector2

from jcspygm_physics.shapes.circle import Circle
from jcspygm_physics.shapes.polygon import Polygon
from jcspygm_physics.manifold import Manifold

import jcs_math
import time
import pygame
import random


class Game(object):
    """
    @class Game
    @brief Main Demo application.
    """

    spriteDir = "../res/sprites/"
    soundDir = "../res/sounds/"

    BGM_SOUND_FADEIN_TIME = 1000 * 1 # in seconds
    BGM_SOUND_FADEOUT_TIME = 1000 * 1 # in seconds

    # override screen path
    JCSPyGm_SceneManager.WHITE_SCREEN_PATH = "./data/white_screen_3840x2160"
    JCSPyGm_SceneManager.BLACK_SCREEN_PATH = "./data/black_screen_3840_2160"

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
    def __init__(self):
        """Constructor."""

        # system specific
        self.gamePause = False

        self.iterations = 10

        self.initialize()

    # --------------------------------------------
    # Public Methods
    # --------------------------------------------
    def run(self, deltaTime, windowInfo):
        """Run the program here."""

        if not self.gamePause:
            self.update(deltaTime)
            self.draw(windowInfo)
        else:
            time.sleep(100)

    def update(self, deltaTime):
        """Update the game logic

        @param float: value of delatTime
        """

        # handle input event.
        self.process_input()

        # update scene manager
        self.sceneManager.update(deltaTime)

        self.step(deltaTime)

    def draw(self, windowInfo):
        """Main render layer graphics

        @param windowInfo: api render device.
        """

        self.sceneManager.draw(windowInfo)

        self.render_contacts(windowInfo)

        label_pos_x = 5
        label_pos_y = 5

        label = self.myfont.render("Click 'Q' to spawn a polygon", 1, (255,255,0))
        windowInfo.blit(label, (label_pos_x, label_pos_y))

        label = self.myfont.render("Click 'W' to spawn a square", 1, (255,255,0))
        windowInfo.blit(label, (label_pos_x, label_pos_y + 20))

        label = self.myfont.render("Click 'E' to spawn a circle", 1, (255,255,0))
        windowInfo.blit(label, (label_pos_x, label_pos_y + 40))

    def initialize(self):
        """Initialize the game."""

        self.sceneManager = JCSPyGm_SceneManager.get_instance()

        self.init_game_scene()

        # set the first scene
        self.sceneManager.switch_scene(self.gameScene)

        self.myfont = pygame.font.SysFont("monospace", 15)

    def process_input(self):
        """Design input here..."""

        if JCSPyGm_Input.get_key_down(pygame.constants.K_e):
            # mouse position
            p1, p2 = pygame.mouse.get_pos()

            tmp_radisu = random.randint(10, 30)

            newCircle = Circle(p1, p2, tmp_radisu)
            self.add_shape_to_scene(newCircle)

        # add random convex polygon
        if JCSPyGm_Input.get_key_down(pygame.constants.K_q):
            # mouse position
            p1, p2 = pygame.mouse.get_pos()
            newPoly = Polygon(p1, p2)
            self.add_shape_to_scene(newPoly)

            vertices_count = random.randint(3, Polygon.MAX_POLY_VERTEX_COUNT)

            tmp_vertices = []  # This is 'Vector2' List.
            for count in range(0, vertices_count):
                tmp_vertices.append(Vector2())

            e = random.randint(5, 20)

            for index in range(0, vertices_count):
                tmp_vertices[index].set_xy(random.randint(-e, e), random.randint(-e, e))

            newPoly.set_rand_convex_poly(tmp_vertices, vertices_count)

            newPoly.restitution = 0.2
            newPoly.dynamic_friction = 0.2
            newPoly.static_friction = 0.4

        # add rectangle or square
        if JCSPyGm_Input.get_key_down(pygame.constants.K_w):

            # mouse position
            p1, p2 = pygame.mouse.get_pos()
            newBox = Polygon(p1, p2)
            self.add_shape_to_scene(newBox)

            newBox.set_box(25, 25)
            newBox.get_rigidbody().set_orientation(random.uniform(-jcs_math.PI, jcs_math.PI))

    def init_game_scene(self):
        """Initialize the game scene."""

        self.gameScene = JCSPyGm_Scene()

        self.gameInterface = JCSPyGm_Interface()

        self.gameInterface.set_friction(1.0)

        # add interface to scene.
        self.gameScene.add_interface(self.gameInterface)

        # --------------------------------------------------

        # manifold list.
        self.contacts = []
        # store all the shape in current scene.
        self.shapes = []

        tmpShape = Circle(200, 200, 30)
        tmpShape.get_rigidbody().set_static()
        self.add_shape_to_scene(tmpShape)

        tmpShape = Polygon(240, 300)
        tmpShape.set_box(200, 10)
        tmpShape.set_orientation(0)
        tmpShape.get_rigidbody().set_static()
        self.add_shape_to_scene(tmpShape)


    def add_shape_to_scene(self, shape):
        """
        Wrap the complex operation into one function.
        @param { Shape } shape : new shape going to be add
        to the scene.
        @return { Shape } : shape have been initialized
        """

        self.shapes.append(shape)

        # add it to the scene
        self.gameInterface.add_game_object(shape)

    def step(self, deltaTime):
        """Step collision check."""

        # Generate new collision info

        # clear all contacs every frame.
        del self.contacts[:]

        for indexA in range(0, len(self.shapes)):

            tmpShapeA = self.shapes[indexA]
            tmpBodyA = tmpShapeA.get_rigidbody()

            for indexB in range(indexA + 1, len(self.shapes)):
                tmpShapeB = self.shapes[indexB]
                tmpBodyB = tmpShapeB.get_rigidbody()

                if (tmpBodyA.get_inverse_mass() == 0 and
                    tmpBodyB.get_inverse_mass() == 0):
                    continue

                tmpManifold = Manifold(tmpShapeA, tmpShapeB)
                tmpManifold.solve()
                if tmpManifold.contact_count > 0:
                    self.contacts.append(tmpManifold)

        # Integrate forces
        for index in range(0, len(self.shapes)):
            Physics.integrate_forces(self.shapes[index], deltaTime)

        # Initialize collision
        for index in range(0, len(self.contacts)):
            self.contacts[index].initialize(deltaTime)

        # Solve Collisions
        for index in range(0, self.iterations):
            for index2 in range(0, len(self.contacts)):
                self.contacts[index2].apply_impulse()

        # Integrate velocities
        for index in range(0, len(self.shapes)):
            Physics.integrate_velocity(self.shapes[index], deltaTime)

        # Corret positions
        for index in range(0, len(self.contacts)):
            self.contacts[index].positional_correction()

        # Clear all forces
        for index in range(0, len(self.shapes)):
            tmpBody = self.shapes[index].get_rigidbody()
            tmpBody.get_force().set_xy(0, 0)
            tmpBody.torque = 0

    def render_contacts(self, windowInfo):
        """Render All Contacts and Normal in order to see how
        physics engine work visually.
        """

        # draw contact point
        contact_point_color = (255, 0, 0)
        point_radius = 2
        for index in range(0, len(self.contacts)):
            tmpManifold = self.contacts[index]
            for index2 in range(0, tmpManifold.contact_count):
                c = tmpManifold.contacts[index2]
                pygame.draw.circle(
                    windowInfo,
                    contact_point_color,
                    (int(c.x), int(c.y)),
                    int(point_radius))


        # draw contact normal
        contact_nomral_color = (0, 255, 0)
        for index in range(0, len(self.contacts)):
            tmpManifold = self.contacts[index]
            n = tmpManifold.normal
            for index2 in range(0, tmpManifold.contact_count):

                c = tmpManifold.contacts[index2]
                c_l = Vector2(c.x, c.y)

                n *= 8
                c_l += n

                line_vertices = []
                line_vertices.append((c.x, c.y))
                line_vertices.append((c_l.x, c_l.y))

                pygame.draw.lines(
                    windowInfo,
                    contact_nomral_color,
                    False,
                    line_vertices)

    # --------------------------------------------
    # Protected Methods
    # --------------------------------------------

    # --------------------------------------------
    # Private Methods
    # --------------------------------------------

    # --------------------------------------------
    # setter / getter
    # --------------------------------------------
