"""
Game Engine for Quoridor
"""
import networkx as nx
from matplotlib import pyplot as plt
from typing import Union, Tuple

# Dit is een test

class Player:
    def __init__(self, name: str):
        self.name = name
        self.game = None
        self.pos = None
        self.turn = None
        self.nrwalls = None
        self.opponent = None
        self.started = None
        self.jumping = False

    def move(self, direction: Union[str, Tuple[int, int]]):
        if isinstance(direction, str):
            x = self.pos[0]
            y = self.pos[1]
            step = (-1) ** int(not self.started)
            if direction == "up":
                y += step
            elif direction == "down":
                y -= step
            elif direction == "left":
                x -= step
            elif direction == "right":
                x += step
            else:
                raise ValueError(
                    "Invalid direction. Must be one of: 'up', 'down', 'left', 'right', or specific coordinates")
        elif isinstance(direction, tuple):
            if len(direction) != 2 or not all(isinstance(coord, int) for coord in direction):
                raise ValueError("Invalid coordinates. Must be a tuple of 2 integers.")
            else:
                x, y = direction
        else:
            raise TypeError("Direction must be a string or a tuple of 2 integers.")

        goal = (x, y)
        if self.game is None:
            print(f"{self.name}, you are currently not playing a game.")
        elif not self.turn:
            print(f"{self.name}, it's not your turn")
        elif x not in range(9) or y not in range(9):
            print(f"{self.name}, you cannot move off the board")
        elif self.pos == goal:
            print(f"{self.name}, you're already standing on that tile")
        elif not self.game.board.has_edge(self.pos, goal):
            print(f"{self.name}, those tiles are not (directly) connected")
        else:
            self.game.move(self, x, y)

    def wall(self, x: int, y: int, vertical: bool):
        goal = (x, y)
        if self.game is None:
            print(f"{self.name}, you are not currently playing a game.")
        elif not self.turn:
            print(f"{self.name}, it's not your turn")
        elif self.nrwalls == 0:
            print(f"{self.name}, you are out of walls")
        elif x == 8 or y == 0 or not (x and y in range(9)):
            print(f"{self.name}, you cannot place a wall outside of the board")
        elif goal in self.game.walls:
            print(f"{self.name}, there's already a wall there")
        elif self.jumping:
            print(f"{self.name}, you can't place a wall since you're jumping over the opponent")
        else:
            p1_free = False
            p2_free = False
            for i in range(9):
                if nx.has_path(self.game.board, self.game.p1.pos, (i, 8)):
                    p1_free = True
                if nx.has_path(self.game.board, self.game.p2.pos, (i, 0)):
                    p2_free = True
            if not (p1_free and p2_free):
                print(
                    f"{self.name}, placing a wall there is not allowed, because you would block {self.opponent} and/or yourself")

            else:
                self.game.wall(self, x, y, vertical)
                self.nrwalls -= 1

    def __str__(self):
        return f"{self.name}: pos={self.pos}, turn={self.turn}, nrwalls={self.nrwalls}"


class Quoridor:
    def __init__(self, player1: Player, player2: Player):
        # Maak een graaf aan die elke tile met zijn buren verbindt
        self.board = nx.grid_graph(dim=(9, 9))
        self.walls = set()
        if player1 == player2:
            raise RuntimeError(f"You can't play against yourself {player1.name}")
        player1.game = self
        player1.pos = (4, 0)
        player1.turn = True
        player1.nrwalls = 10
        player1.started = True
        player1.opponent = player2

        self.p1 = player1
        player2.game = self
        player2.pos = (4, 8)
        player2.turn = False
        player2.nrwalls = 10
        player2.started = False
        player2.opponent = player1
        self.p2 = player2
        self.players = {self.p1, self.p2}

    def move(self, player: Player, x: int, y: int):
        player.pos = (x, y)
        if player.opponent.pos == (x, y):
            player.jumping = True
            print(f"Move from {player.name} succesful and you can move once more since you will jump over the opponent")
            self.show()
        else:
            player.turn = False
            player.opponent.turn = True
            print(f"Move from {player.name} succesful")
            self.show()
    def wall(self, player: Player, x: int, y: int, vertical: bool):
        """
        :param player: the player placing the wall
        :param x: x-coord of right corner of the 4 nodes that determine a wall
        :param y: y-coord of right corner of the 4 nodes that determine a wall
        :param vertical: wall is standing vertical in the perspective of the two players
        :return: 
        """
        goal = (x, y)
        self.walls.add(goal)
        if vertical:
            self.board.remove_edge(goal, (x + 1, y))
            self.board.remove_edge((x, y - 1), (x + 1, y - 1))
        else:
            self.board.remove_edge(goal, (x, y - 1))
            self.board.remove_edge((x + 1, y), (x + 1, y - 1))

        player.turn = False
        player.opponent.turn = True
        print(f"Wall placement succesful")
        self.show()

    def __str__(self):
        status = "_" * 15 + "Current game status" + "_" * 15 + "\n"
        status = status + str(self.board) + "\n" + str(self.p1) + "\n" + str(self.p2) + "\n" + "_" * 49
        return status

    def show(self):
        plt.figure(figsize=(6, 6))
        pos = {(x, y): (x, y) for x, y in self.board.nodes()}
        labels = {(x, y): f"{x} {y}" for x, y in self.board.nodes()}
        labels[self.p1.pos] = self.p1.name
        labels[self.p2.pos] = self.p2.name
        nx.draw(self.board, pos=pos,
                node_color='grey',
                with_labels=True,
                labels=labels,
                node_size=1000,
                node_shape="s")
        plt.show()


if __name__ == "__main__":
    Rune = Player("Rune")
    Pieter = Player("Pieter")
    game = Quoridor(Pieter, Rune)
    game.show()
    Pieter.move("up")
    Rune.move((4, 7))
    Rune.move("down")

    Pieter.move("right")
    Rune.move("down")
    Pieter.move("left")
    Rune.move("left")
    Rune.wall(4, 3, True)
    Pieter.wall(4, 3, True)
    Rune.move("down")
    Rune.move("up")
    Pieter.move("up")
    Rune.move("up")
    Pieter.move("right")
