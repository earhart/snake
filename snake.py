#!/usr/bin/env python

# Importing these modules makes them visible in the current file
import pygame
import random

# Basic setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Game setup

# We use a variable to keep track of whether the game is done or not.
done = False

# We use an event and a timer to figure out when to move the snake.
# This decouples the movement speed from the frame rate.
move_snake_event_type = pygame.event.custom_type()
move_snake_event = pygame.event.Event(move_snake_event_type)
pygame.time.set_timer(move_snake_event, 100)  # 100ms -> 10 boxes per second

# We need to keep track of the current snake direction.  To keep
# things simple, let's just reuse the WASD key values.
current_direction = pygame.K_d

# BOX_PX gives us a scaling for the boxes that make up the snake.
BOX_PX = 20

# Based on BOX_PX and the screen, we can calculate the size of the
# playfield -- note that we're keeping the playfield in
# game-coordinates, though, not pixel-coordinates.

playfield = screen.get_rect()
playfield.width //= BOX_PX
playfield.height //= BOX_PX

# We also need to keep track of the boxes occupied by the snake.  Each
# entry in the list is the game grid coordinate (x, y) occupied by
# that snake part; the head of the snake is the first entry in the
# list.  We start the snake as a single box.
snake = [playfield.center]


# And let's set the position of the apple.
#
# This is a little tricky, since we don't want the apple to
# materialize within the snake; also, we need to do this every time
# the snake eats the apple.
#
# So: we create a little helper routine that knows how to make an
# apple position, and then we use it to set the initial apple
# position.
def make_apple_pos():
    while True:
        pos = (
            random.randrange(playfield.left, playfield.right),
            random.randrange(playfield.top, playfield.bottom),
        )
        if pos not in snake:
            return pos


apple = make_apple_pos()


# Okay, here's the main game loop.  Note that we don't test for
# whether the game is done or not here (because "done" is always False
# here); instead, we test for whether "done" is set in the middle of
# the loop.
while True:
    # Poll for events, updating the game world state.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # The user closed the window; we're done.
            done = True

            # Stop processing events.
            break

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                current_direction = event.key

        if event.type == move_snake_event_type:
            # Move the snake in the current direction.
            x, y = snake[0]
            if current_direction == pygame.K_w:
                y -= 1
            elif current_direction == pygame.K_a:
                x -= 1
            elif current_direction == pygame.K_s:
                y += 1
            elif current_direction == pygame.K_d:
                x += 1

            if not playfield.collidepoint(x, y):
                # We're off the edge!
                done = True
                break

            # Check for collision with apple
            if (x, y) == apple:
                # We ate the apple.
                apple = make_apple_pos()
            else:
                # Since we didn't eat the apple, shrink the snake.
                snake.pop()

            # Check for collision with the snake (now that we've removed
            # the tail of the snake, if that was necessary).
            if (x, y) in snake:
                done = True
                break

            # Prepend the new head coordinate to the snake.
            snake.insert(0, (x, y))

    if done:
        # We're done; don't bother rendering the next frame, just exit
        # the loop.
        break

    # Draw the user's view based on the current game world state.

    # First, we wipe the scren
    screen.fill("white")

    # Next, draw a square for every body part of the snake.
    for x, y in snake:
        pygame.draw.rect(
            screen, "darkgreen", pygame.Rect(x * BOX_PX, y * BOX_PX, BOX_PX, BOX_PX)
        )

    # Finally, draw the apple.
    pygame.draw.rect(
        screen, "red", pygame.Rect(apple[0] * BOX_PX, apple[1] * BOX_PX, BOX_PX, BOX_PX)
    )

    # Done drawing, so flip the screen - double-buffering like this
    # makes it so that the user doesn't see a partial update as it's
    # being drawn.
    pygame.display.flip()

    clock.tick(60)  # Run at 60 FPS

# After the loop completes, we want to gracefully tear down
# the game state (including the game window).
pygame.quit()
