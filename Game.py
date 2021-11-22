import pygame

from GameState import GamesState
from ScoreState import ScoreState
from MainMenuState import MainMenuState
from PauseState import PauseState
from InstructionsState import InstructionsState

# The Game class controls which state of the game runs. The main menu, game, pause menu, score menu, and instructions
# menu are each different states that also have their own class. When the game wants to run a certain state, it
# places it in the state_queue and runs the first element in that list. Because each state has their own internal
# loop, once that internal loop is over we can assume that the state is no longer needed so it is deleted from the list.
# The only exception is the game state, which if paused, will remain in the list but a pause state will be put in front
# of it on the list and that will run instead.

# Music and sound is controlled by the individual states and classes.


class Game:
    def __init__(self, window):
        self.window = window
        self.current_state = "Main_Menu"
        self.state_queue = []
        self.stats = None

    def run(self):
        while True:
            self.state_manager()

# state_check checks to see if there are any objects whose type matches the state_class given and returns a list with
# the first element being either a true or false depending on if a match is found, and the second being an index of the
# found match or 0 if no match was found

    def state_check(self, state_class):
        if self.state_queue:
            for state in self.state_queue:
                if type(state) is state_class:
                    return [True, self.state_queue.index(state)]
        return [False, 0]

# The state_manager checks to see what the current_state is (current_state can be changed by the next_state
# variable all states have) and checks to see if an object is in the state_queue whose type matches the current_state.
# If there is that object is moved to the front of the list. If not it creates an object with that type and puts it
# first on the state_queue.

    def state_manager(self):
        if self.current_state == "Main_Menu":
            present_location = self.state_check(MainMenuState)
            if present_location[0]:
                if present_location[1] != 0:
                    self.state_queue.insert(0, self.state_queue.pop(present_location[1]))
            else:
                self.state_queue.insert(0, MainMenuState(self.window))

        if self.current_state == "Game":
            present_location = self.state_check(GamesState)
            if present_location[0]:
                if present_location[1] != 0:
                    self.state_queue.insert(0, self.state_queue.pop(present_location[1]))
            else:
                self.state_queue.insert(0, GamesState(self.window))

        if self.current_state == "Score":
            present_location = self.state_check(ScoreState)
            if present_location[0]:
                if present_location[1] != 0:
                    self.state_queue.insert(0, self.state_queue.pop(present_location[1]))
            else:
                self.state_queue.insert(0, ScoreState(self.window, self.stats))

        if self.current_state == "Pause":
            present_location = self.state_check(PauseState)
            if present_location[0]:
                if present_location[1] != 0:
                    self.state_queue.insert(0, self.state_queue.pop(present_location[1]))
            else:
                self.state_queue.insert(0, PauseState(self.window))

        if self.current_state == "Instructions":
            present_location = self.state_check(InstructionsState)
            if present_location[0]:
                if present_location[1] != 0:
                    self.state_queue.insert(0, self.state_queue.pop(present_location[1]))
            else:
                self.state_queue.insert(0, InstructionsState(self.window))

        self.state_queue[0].run_state()

        if self.current_state == "Game" and not self.state_queue[0].get_paused():
            self.stats = self.state_queue[0].get_stats()

        self.current_state = self.state_queue[0].next_state

        if type(self.state_queue[0]) == PauseState:
            if self.current_state == "Main_Menu":
                for state in self.state_queue:
                    if type(state) == GamesState:
                        self.state_queue.remove(state)

        if type(self.state_queue[0]) != GamesState:
            self.state_queue.pop(0)
        elif type(self.state_queue[0]) == GamesState and not self.state_queue[0].get_paused():
            self.state_queue.pop(0)


