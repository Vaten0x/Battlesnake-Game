# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "Vaten",  # TODO: Your Battlesnake Username
    "color": "#301934",  # TODO: Choose color
    "head": "happy",  # TODO: Choose head
    "tail": "curled",  # TODO: Choose tail
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  # We've included code to prevent your Battlesnake from moving backwards
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    is_move_safe["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    is_move_safe["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    is_move_safe["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    is_move_safe["up"] = False

  # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds

  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  #you have to decrement them since we are trying to find the maximum board width and height where here these arrays gives the values from 1 to 12 if the board was 11 x 11. So, to find the max, we need to decrement them.
  board_width -= 1
  board_height -= 1

  #Here it was just for testing, figuring out what the values are.
  #print(board_width)
  #print(board_height)
  #print(my_head["x"])

  #Here when snake is on the left wall, it makes snake not to go left
  if my_head["x"] == 0:

    is_move_safe["left"] = False

  #Here when snake is on the top wall, it makes snake not to go up
  if my_head["x"] == board_width:

    is_move_safe["right"] = False

  #Here when snake is on the right wall, it makes snake not to go right
  if my_head["y"] == board_height:

    is_move_safe["up"] = False

  #Here when snake is on the bottom wall, it makes snake not to go down
  if my_head["y"] == 0:

    is_move_safe["down"] = False

  #The if statements now deals if when the snake is at the bottom:

  #This makes the snake doesn't go left or down when the snake is at bottom left
  if my_head["x"] == 0 and my_head["y"] == 0:

    is_move_safe["left"] = False
    is_move_safe["down"] = False

  #This makes the snake doesn't go left or up when the snake is at top left
  if my_head["x"] == 0 and my_head["y"] == board_height:

    is_move_safe["left"] = False
    is_move_safe["up"] = False

  #This makes the snake doesn't go right or up when the snake is at top right

  if my_head["x"] == board_width and my_head["y"] == board_height:

    is_move_safe["right"] = False
    is_move_safe["up"] = False

  #This makes the snake doesn't go right or down when the snake is at bottom right

  if my_head["x"] == board_width and my_head["y"] == board_height:

    is_move_safe["right"] = False
    is_move_safe["down"] = False

  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself

  my_body = game_state['you']['body']

  #these are some variables that can be used easier to implement in coding at the bottom with if then statements since it's easier to track which one to use since these all variables represents a point in terms of x or y. For example, body_on_left will represent the square on the left side of my snake's head. and other variables will be perpendicular to the head also. I found this easier to track.
  body_on_left = my_head["x"] - 1
  body_on_right = my_head["x"] + 1

  body_on_top = my_head["y"] + 1
  body_on_bottom = my_head["y"] - 1

  for body in my_body:
    #Here it was just for testing, figuring out what the values are.
    #print(body)

    #if my snake's body is on the left side, we have to avoid it by setting the move to the left is unsafe
    if body_on_left == body["x"] and my_head["y"] == body["y"]:
      is_move_safe["left"] = False

    #if my snake's body is on the right side, we have to avoid it by setting the move to the right is unsafe
    if body_on_right == body["x"] and my_head["y"] == body["y"]:
      is_move_safe["right"] = False

    #if my snake's body is on the top side, we have to avoid it by setting the move to the up is unsafe
    if my_head["x"] == body["x"] and body_on_top == body["y"]:
      is_move_safe["up"] = False

    #if my snake's body is on the bottom side, we have to avoid it by setting the move to the down is unsafe
    if my_head["x"] == body["x"] and body_on_bottom == body["y"]:
      is_move_safe["down"] = False

  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  opponents = game_state['board']['snakes']

  #these variables are to expect if the opponents are off by 2 blocks but with same move, it can cause head to head collisions, so we have to avoid it.
  expect_opponent_head_left = my_head["x"] - 2
  expect_opponent_head_right = my_head["x"] + 2
  expect_opponent_head_top = my_head["x"] + 2
  expect_opponent_head_bottom = my_head["y"] - 2

  #since there are many opponents, we need to go through one by one of every snake's body coordinates
  for avoid_others in opponents:

    #now we seperate each snake's body coordinates into pieces in one by one, so we can check each of them
    for opponent_body in avoid_others['body']:

      #this is to avoid head to head collisions with other snakes
      opponent_head = avoid_others['head']

      #checks so if this is my snake or the opponent's snake, we already took methods on how to avoid our body, so we have to exclude it from this for loop
      if opponent_head["x"] != my_head["x"] or opponent_head["y"] != my_head[
          "y"]:

        #testing
        #print(opponent_body)
        #print(my_head["x"])
        #print(my_head["y"])

        #checks if the opponent's body is on the left side of the head
        if body_on_left == opponent_body["x"] and my_head[
            "y"] == opponent_body["y"]:
          is_move_safe["left"] = False

        #checks if the opponent's body is on the right side of the head
        if body_on_right == opponent_body["x"] and my_head[
            "y"] == opponent_body["y"]:
          is_move_safe["right"] = False

        #checks if the opponent's body is on the top side of the head
        if my_head["x"] == opponent_body["x"] and body_on_top == opponent_body[
            "y"]:
          is_move_safe["up"] = False

        #checks if the opponent's body is on the bottom side of the head
        if my_head["x"] == opponent_body[
            "x"] and body_on_bottom == opponent_body["y"]:
          is_move_safe["down"] = False

        #checks if the opponent's head is on the left side of the head note that this is different from the if statements of checking the opponent's body nearby
        if body_on_left == opponent_head["x"] and my_head[
            "y"] == opponent_head["y"]:
          is_move_safe["left"] = False

        #checks if the opponent's head is on the left side of the head
        if body_on_right == opponent_head["x"] and my_head[
            "y"] == opponent_head["y"]:
          is_move_safe["right"] = False

        #checks if the opponent's head is on the top side of the head
        if my_head["x"] == opponent_head["x"] and body_on_top == opponent_head[
            "y"]:
          is_move_safe["up"] = False

        #checks if the opponent's head is on the bottom side of the head
        if my_head["x"] == opponent_head[
            "x"] and body_on_bottom == opponent_head["y"]:
          is_move_safe["down"] = False

        #checks if the opponent's head is on the left side of the head by two blocks, if so, don't turn left to avoid head to head collisions
        if expect_opponent_head_left == opponent_head["x"] and my_head[
            "y"] == opponent_head["y"]:
          is_move_safe["left"] = False

        #checks if the opponent's head is on the right side of the head by two blocks, if so, don't turn right to avoid head to head collisions
        if expect_opponent_head_right == opponent_head["x"] and my_head[
            "y"] == opponent_head["y"]:
          is_move_safe["right"] = False

        #checks if the opponent's head is on the top side of the head by two blocks, if so, don't turn up to avoid head to head collisions
        if my_head["x"] == opponent_head[
            "x"] and expect_opponent_head_top == opponent_head["y"]:
          is_move_safe["up"] = False

        #checks if the opponent's head is on the bottom side of the head by two blocks, if so, don't turn down to avoid head to head collisions
        if my_head["x"] == opponent_head[
            "x"] and expect_opponent_head_bottom == opponent_head["y"]:
          is_move_safe["down"] = False

        #now we make predictions based on what the opponents will make move on, when the opponent's head is near and off by 1 in x and y, we avoid the head collisions for each scenarios

        #this is when the opponent's head is on the top left side, then we must avoid going left AND up since it could cause head to head collisions
        if body_on_left == opponent_head["x"] and body_on_top == opponent_head[
            "y"]:

          is_move_safe["left"] = False
          is_move_safe["up"] = False

        #this is when the opponent's head is on the bottom left side, then we must avoid going left AND down since it could cause head to head collisions
        if body_on_left == opponent_head[
            "x"] and body_on_bottom == opponent_head["y"]:

          is_move_safe["left"] = False
          is_move_safe["down"] = False

        #this is when the opponent's head is on the bottom right side, then we must avoid going right AND down since it could cause head to head collisions
        if body_on_right == opponent_head[
            "x"] and body_on_bottom == opponent_head["y"]:

          is_move_safe["right"] = False
          is_move_safe["down"] = False

        #this is when the opponent's head is on the top right side, then we must avoid going right AND down since it could cause head to head collisions
        if body_on_right == opponent_head[
            "x"] and body_on_top == opponent_head["y"]:
          is_move_safe["right"] = False
          is_move_safe["up"] = False

  # Are there any safe moves left?

  if is_move_safe["left"] == False and is_move_safe[
      "right"] == False and is_move_safe["up"] == False and is_move_safe[
        "down"] == False:

    print("No safe moves detected! Moving in risky move")

    #Here we turn all the safe moves off since we don't have a good choice, so we turn off the maximizing move strategy for loop, so we can make a risky move to still go on rather than making a one bad move (just going down won't help) This turns on all of the expected head collisions is_move_safe back to true again. So it reverts all calculations of potential solution.

    #set back to True for all boolean again
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    #same code for not making it go backward
    if my_neck["x"] < my_head["x"]:
      is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:
      is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:
      is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:
      is_move_safe["up"] = False

    #check if it's near a wall again
    if my_head["x"] == 0:
      is_move_safe["left"] = False
    if my_head["x"] == board_width:
      is_move_safe["right"] = False
    if my_head["y"] == board_height:
      is_move_safe["up"] = False
    if my_head["y"] == 0:
      is_move_safe["down"] = False
    if my_head["x"] == 0 and my_head["y"] == 0:
      is_move_safe["left"] = False
      is_move_safe["down"] = False
    if my_head["x"] == 0 and my_head["y"] == board_height:
      is_move_safe["left"] = False
      is_move_safe["up"] = False
    if my_head["x"] == board_width and my_head["y"] == board_height:
      is_move_safe["right"] = False
      is_move_safe["up"] = False
    if my_head["x"] == board_width and my_head["y"] == board_height:
      is_move_safe["right"] = False
      is_move_safe["down"] = False

    #check for near own body segments again
    for body in my_body:
      if body_on_left == body["x"] and my_head["y"] == body["y"]:
        is_move_safe["left"] = False
      if body_on_right == body["x"] and my_head["y"] == body["y"]:
        is_move_safe["right"] = False
      if my_head["x"] == body["x"] and body_on_top == body["y"]:
        is_move_safe["up"] = False
      if my_head["x"] == body["x"] and body_on_bottom == body["y"]:
        is_move_safe["down"] = False

    #check for nearby opponent's body segments/head again, you don't make predictions this time
    for avoid_others in opponents:
      for opponent_body in avoid_others['body']:
        opponent_head = avoid_others['head']
        if opponent_head["x"] != my_head["x"] or opponent_head["y"] != my_head[
            "y"]:
          if body_on_left == opponent_body["x"] and my_head[
              "y"] == opponent_body["y"]:
            is_move_safe["left"] = False
          if body_on_right == opponent_body["x"] and my_head[
              "y"] == opponent_body["y"]:
            is_move_safe["right"] = False
          if my_head["x"] == opponent_body[
              "x"] and body_on_top == opponent_body["y"]:
            is_move_safe["up"] = False
          if my_head["x"] == opponent_body[
              "x"] and body_on_bottom == opponent_body["y"]:
            is_move_safe["down"] = False
          if body_on_left == opponent_head["x"] and my_head[
              "y"] == opponent_head["y"]:
            is_move_safe["left"] = False
          if body_on_right == opponent_head["x"] and my_head[
              "y"] == opponent_head["y"]:
            is_move_safe["right"] = False
          if my_head["x"] == opponent_head[
              "x"] and body_on_top == opponent_head["y"]:
            is_move_safe["up"] = False
          if my_head["x"] == opponent_head[
              "x"] and body_on_bottom == opponent_head["y"]:
            is_move_safe["down"] = False

  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  #if there are no safe moves left, we call out that we are going to make a risky move
  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    return {"move": "down"}

  # Choose a random move from the safe ones
  next_move = random.choice(safe_moves)

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer

  food = game_state['board']['food']
  minimizing_turn_for_food = 100
  minimizing_x_coordinate_food = 0
  minimizing_y_coordinate_food = 0

  #if there are more than one safe move to choose, meaning it's safe to choose a random move. This finds the snake's minimizing turn needed to get the food, but this still considers 'living' or 'avoiding' as a higher priority.
  if len(safe_moves) > 1:

    #we check every food coordinates one by one:
    for food_coordinate in food:

      #this is the equation for finding the distance between the two points, the head and the food. Here we used the absolute value function rather than using the square root or power to make the equation simpler
      turns_needed_to_reach = abs(my_head["x"] - food_coordinate["x"]) + abs(
        my_head["y"] - food_coordinate["y"])

      if (minimizing_turn_for_food > turns_needed_to_reach):
        minimizing_turn_for_food = turns_needed_to_reach
        #we get the minimizing x and y coordinate of the food, so that we can track and let the snake eat them.
        minimizing_x_coordinate_food = food_coordinate["x"]
        minimizing_y_coordinate_food = food_coordinate["y"]

  if len(safe_moves) > 1:
    #for testing:
    #print(my_head["x"])
    #print(minimizing_x_coordinate_food)
    #print(my_head["y"])
    #print(minimizing_y_coordinate_food)

    #if the nearest food is on the right side, we move right rather then going random move
    if my_head["x"] > minimizing_x_coordinate_food and is_move_safe[
        "left"] == True:
      is_move_safe = {"up": False, "down": False, "left": True, "right": False}

    #if the nearest food is on the right side, we move right rather then going random move
    elif my_head["x"] < minimizing_x_coordinate_food and is_move_safe[
        "right"] == True:
      is_move_safe = {"up": False, "down": False, "left": False, "right": True}

    #if the nearest food is on the top side, we move up rather then going random move
    elif my_head["y"] < minimizing_y_coordinate_food and is_move_safe[
        "up"] == True:
      is_move_safe = {"up": True, "down": False, "left": False, "right": False}

    #if the nearest food is on the bottom side, we move down rather then going random move
    elif my_head["y"] > minimizing_y_coordinate_food and is_move_safe[
        "down"] == True:
      is_move_safe = {"up": False, "down": True, "left": False, "right": False}

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})
