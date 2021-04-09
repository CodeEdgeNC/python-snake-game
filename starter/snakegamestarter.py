# Snake Game with Python using Pygame
#
# In this workshop you will learn how to build the game Snake.
# The is an arcade game and it has very simple logic.
#
# The snake is represented as snake (red blocks), which grows if it eats
# an apple (green block). The goal of the game is to eat as many apples
# as possible without colliding into itself or the edge of the screen.
# This is very easy in the early phase of the game but is increasingly
# more difficult as the length of the snake grows.


# Below are modules that are imported into our solution.
# These modules have predefined code that will be used
# by this solution.
from pygame.locals import *
from random import randint
import time
import os
import shelve
import tkinter.messagebox
# Todo: 1. Import the pygame module

# Todo: 2. Create the Apple Class


class Snake:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
    updateCountMax = 2
    updateCount = 0
    # Todo: 3. Create variables to define the window width and height


    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:      # Move Right
                self.x[0] = self.x[0] + self.step
                if self.windowWidth < self.x[0]:
                    self.x[0] = self.windowWidth - self.x[0]

            if self.direction == 1:      # Move Left
                self.x[0] = self.x[0] - self.step
                if self.x[0] < 0:
                    self.x[0] = self.windowWidth - self.x[0]

            if self.direction == 2:      # Move Down
                self.y[0] = self.y[0] - self.step
                if self.y[0] < 0:
                    self.y[0] = self.windowHeight + self.y[0]

            if self.direction == 3:      # Move Up
                self.y[0] = self.y[0] + self.step
                if self.y[0] > self.windowHeight:
                    self.y[0] = self.windowHeight - self.y[0]

            self.updateCount = 0

    # TODO: 4 Create  Methods in the Snake class to control the direction of the snake


    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

class App:
    windowWidth = 800
    windowHeight = 600
    snake = 0
    apple = 0
    highscore = ""

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.snake = Snake(3)
        self.apple = Apple(5, 5)

    def on_init(self):

        # initialize the pygame library
        pygame.init()

        # Play Music
        # pygame.mixer_music.load("gamemusic.wav")

        # Set the game drawing surface
        self._display_surf = pygame.display.set_mode(
            (self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        # Set the title of the window
        pygame.display.set_caption(
            'Youth Innovation Summit Programming Workshop - Snake Game')
        self._running = True

        # Load the snake and apple images
        self._image_surf = pygame.image.load("redblock.jpg").convert()
        self._apple_surf = pygame.image.load("greenblock.jpg").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.snake.update()

        # does snake eat apple?
        for i in range(0, self.snake.length):
            if self.game.isCollision(
                    self.apple.x, self.apple.y, self.snake.x[i], self.snake.y[i], 44):
                # Move the Apple to a new location
                self.apple.x = randint(2, 9) * 44
                self.apple.y = randint(2, 9) * 44

                # Add 1 block to the length of the Snake
                self.snake.length = self.snake.length + 1

        # Get access to high score file
        highScoreFile = shelve.open('score.txt')

        # does snake collide with itself?
        for i in range(2, self.snake.length):
            if self.game.isCollision(
                    self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i], 40):

                highscore = highScoreFile['score']  # Read highscore from disk

                if self.snake.length <= highscore:
                    highscoretext = "Your score is " + str(self.snake.length) + '\r\r' + \
                                    "The high score is: " + str(highscore)
                else:
                    highscoretext = "New High Score!!! \r Your score is " + \
                        str(self.snake.length)
                    # Save new high score
                    highScoreFile['score'] = self.snake.length

                # Show Message Box to indicate that the game is over
                root = tkinter.Tk()     # get access to root tk window
                root.withdraw()         # do not display extra root tk window
                # tkinter.messagebox.showinfo('Game Over!',
                # highscoretext + '\r\r')

                answer = tkinter.messagebox.askyesno(
                    "Game Over", highscoretext + '\r\r' + "Do you want to reset the highscore?", )
                if answer == False:
                    highScoreFile.close()
                    exit(0)
                else:
                    # Save new high score
                    highScoreFile['score'] = 0
                    highScoreFile.close()
                    self.snake.length = 3
                    exit(0)
        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.snake.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def load_image(name, colorkey=None):
        fullname = os.path.join('images', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print
            'Cannot load image:', name
            raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        # play music while game is running
        # pygame.mixer.music.play(10)

        # TODO: 5 - Create a “while ” Loop in the App Class


            # TODO: 6 - Add if conditional statements to control the snake direction


            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
