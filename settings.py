class Settings:
    # Class that stores settings for alien invasion

    def __init__(self):
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (248, 5, 5)
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

