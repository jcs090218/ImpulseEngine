#  ========================================================================
#  $File: test_app.py $
#  $Date: 2017-01-15 23:27:42 $
#  $Revision: $
#  $Creator: Jen-Chieh Shen $
#  $Notice: See LICENSE.txt for modification and distribution information
#                    Copyright (c) 2017 by Shen, Jen-Chieh $
#  ========================================================================


#from jcspygm_physics.game import Game

import jcspygm_physics.game
from jcspygm.core.JCSPyGm_Application import JCSPyGm_Application


class TestApp_Physics(JCSPyGm_Application):
    """
    @class Test application
    @brief Application for testing purpose.
    """

    __testGame = None
    __appTitle = "JCSPyGm Physics"

    def __init__(self):
        """Constructor."""

        # call the base constructor
        super(TestApp_Physics, self).__init__()

        self.__testGame = jcspygm_physics.game.Game()

        # NOTE(jenchieh): here is how u set the title.
        self.get_window().set_window_title(self.__appTitle)

        self.get_window().update_window_title()

        # here is how u decide to show the window info.
        self.set_show_frame_rate(True)

    def _run_app(self, deltaTime, windowInfo):
        """Run the application."""

        self.get_game().run(deltaTime, windowInfo)

    def get_game(self):
        """Return the game itself."""
        return self.__testGame
