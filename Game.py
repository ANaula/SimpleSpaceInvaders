import pygame

from GameState import GamesState
from ScoreState import ScoreState
from MainMenuState import MainMenuState
from PauseState import PauseState
from InstructionsState import InstructionsState


class Game:
    def __init__(self, window):
        self.window = window
        self.current_state = "Main_Menu"
        self.state_queue = []
        self.stats = None

    def run(self):
        while True:
            self.state_manager()

    def state_check(self, state_class):
        if self.state_queue:
            for state in self.state_queue:
                if type(state) is state_class:
                    return [True, self.state_queue.index(state)]
        return [False, 0]

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


# how to play state, sounds, export
