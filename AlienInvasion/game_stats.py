class GameStats:
    """track stats for alien invasion"""

    def __init__(self,ai_game):
        #Initialise Stats
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invasion in an active Stats
        self.game_active = False

    def reset_stats(self):
        """initialise stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
