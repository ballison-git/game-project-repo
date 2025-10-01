import pygame.font

class Button:
    def __init__(self,ai_game,msg,color,width,height):
        """initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set dimensions and properties of the button
        self.width, self.height = width, height
        self.button_color = color
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        #build button rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        #button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw a blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

    def draw_button_custom(self,x,y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.msg_image_rect.center = self.rect.center
        #Draw blank button and message where creator chooses
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

