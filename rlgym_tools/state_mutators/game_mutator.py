from typing import Dict, Any

from rlgym.api import StateMutator
from rlgym.rocket_league.api import GameState, Car
from rlgym.rocket_league.state_mutators import KickoffMutator

from rlgym_tools.shared_info_providers.scoreboard_provider import ScoreboardInfo


class GameMutator(StateMutator[GameState]):
    def __init__(self, game_length_seconds: float = 300.0, kickoff_timer_seconds: float = 5.0):
        self.game_length_seconds = game_length_seconds
        self.kickoff_timer_seconds = kickoff_timer_seconds
        self.kickoff_mutator = KickoffMutator()

    def apply(self, state: GameState, shared_info: Dict[str, Any]) -> None:
        scoreboard: ScoreboardInfo = shared_info["scoreboard"]

        scoreboard.game_timer_seconds = self.game_length_seconds
        scoreboard.kickoff_timer_seconds = self.kickoff_timer_seconds
        scoreboard.blue_score = 0
        scoreboard.orange_score = 0
        scoreboard.go_to_kickoff = True
        scoreboard.is_over = False
        
        print("Going to kickoff (in game_mutator)")
        self.kickoff_mutator.apply(state, shared_info)

        assert state.ball.position[1] == 0, "Ball is not in kickoff position"
        car: Car = next(iter(state.cars.items()))[1]
        assert car.physics.linear_velocity[0] == 0, "Car is not kickoff ready"


        scoreboard.kickoff_timer_seconds = self.kickoff_timer_seconds
        scoreboard.go_to_kickoff = False
