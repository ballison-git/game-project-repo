import sys
from time import sleep

import pygame

from star import Star
from random import randint
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #overall class to manage game assets and behaviour
    def __init__(self):
        #Initialising the game and creating game resources
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.stats = GameStats(self)

        self._create_star_fleet()
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self,"Play")

        #set the background colour
        self.bg_color = self.settings.bg_color

    def run_game(self):
        #start the main loop for the game
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        #responds to keypresses and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self, event):
        #respond to keypresses
        if event.key == pygame.K_RIGHT:
            # move ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # move ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            #fire bullet
            if len(self.bullets) < self.settings.bullets_allowed:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        #responds to key releases
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game if the player clicks button rectangle"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Call start game to begin game
            self._start_game()

    def _start_game(self):

        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """Respond to ship being hit by alien"""
        #decrement ships left
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _fire_bullet(self):
        #create new bullet and add to bullets group
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

# ALIEN FLEET

    def _create_fleet(self):
        #create fleet of aliens
        #make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen.get_rect().width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine number of rows of aliens to fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.screen.get_rect().height -
                             (2 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create alien & place it in the row
        alien = Alien(self)
        #determine alien width and height, save values
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge
        then update the positions of all aliens"""

        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #Look for aliens at bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > screen_rect.bottom:
                #Treat the same as ship hit
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        #Respond if aliens have reached the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

# STAR SYSTEM

    def _create_star_fleet(self):
        #make a star
        star = Star(self)
        star_width, star_height = star.rect.size
        star_space_x = self.screen.get_rect().width
        number_stars_x = star_space_x // (2 * star_width)

        #determine number of rows for stars
        star_space_y = self.screen.get_rect().height - (2 * star_height)
        number_star_rows = star_space_y // (2 * star_height)

        for row in range(number_star_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, randint(-10,10))


    def _create_star(self, star_number, row_number):
        #create star and place in the row
        star = Star(self)
        #get star width and height
        star_width, star_height = star.rect.size
        star.x = star_width + 2 * star_width * star_number
        star.rect.x = star.x
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number
        self.stars.add(star)

    def _update_screen(self):
        # updates images on a screen, and flips to the new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.stars.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw play button if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make the most recently drawn screen visible
        pygame.display.flip()

    def _update_bullets(self):
        #update bullet positions
        self.bullets.update()

        # remove bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullet collisions with aliens
        # If so get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create a new row of aliens
            self.bullets.empty()
            self._create_fleet()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()