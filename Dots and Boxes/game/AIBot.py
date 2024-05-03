<<<<<<< HEAD
from time import time
from Action import Action
from State import State
from typing import List
import numpy as np

Late = 0.5


class AIBot():

    
    def __init__(self, dots: int):
        self.isPlayer1 = True
        self.totalTime = 0
        self.n = dots - 1

   # == transition model == #
    def transitionModel(self, Node: State) -> Action:

        self.isPlayer1 = Node.player1Turn
        BestAction = None
        self.totalTime = time() + Late

        EmptyRows = np.count_nonzero(Node.rowStatus == 0)
        EmptyColumns = np.count_nonzero(Node.colStatus == 0)
        
        for depth in range(EmptyRows + EmptyColumns):
            try:
                # all child of node
                actions = self.successor_function(Node)
                utilities = np.array(
                    [self.MiniMaxAlg(self.new_State(Node, action), max_depth=depth + 1) for action in actions])
                index = np.random.choice(np.flatnonzero(utilities == utilities.max()))
                BestAction = actions[index]

            except TimeoutError:
                break
       
        return BestAction

    
    def successor_function(self, Node: State) -> List[Action]:
        rows = self.validPositions(Node.rowStatus)
        cols = self.validPositions(Node.colStatus)
        actions: List[Action] = []

        for Position in rows:
            actions.append(Action("row", Position))
        for Position in cols:
            actions.append(Action("col", Position))

        return actions

    
    def validPositions(self, Array: np.ndarray):
        [Ys, Xs] = Array.shape
        ValidPos: List[tuple[int, int]] = []

        for y in range(Ys):
            for x in range(Xs):
                if Array[y, x] == 0:
                    ValidPos.append((x, y))

        return ValidPos

    # == Update board
    def new_State(self, Node: State, newActon: Action) -> State:
        type = newActon.Type
        x, y = newActon.Position

        new_Node = State(
            Node.boardStatus.copy(),
            Node.rowStatus.copy(),
            Node.colStatus.copy(),
            Node.player1Turn,
        )

        player_flag = -1 if new_Node.player1Turn else 1

        hasNewScore = False
        point = 1

        [Ys, Xs] = new_Node.boardStatus.shape


        if y < Ys and x < Xs:
            new_Node.boardStatus[y, x] = (abs(new_Node.boardStatus[y, x]) + point) * player_flag
            if abs(new_Node.boardStatus[y, x]) == 4:
                hasNewScore = True


        if type == "row":
            new_Node.rowStatus[y, x] = 1
            if y > 0:
                new_Node.boardStatus[y - 1, x] = (abs(new_Node.boardStatus[y - 1, x]) + point) * player_flag
                if abs(new_Node.boardStatus[y - 1, x]) == 4:
                    hasNewScore = True


        elif type == "col":
            new_Node.colStatus[y, x] = 1
            if x > 0:
                new_Node.boardStatus[y, x - 1] = (abs(new_Node.boardStatus[y, x - 1]) + point) * player_flag
                if abs(new_Node.boardStatus[y, x - 1]) == 4:
                    hasNewScore = True

        new_Node = new_Node._replace(player1Turn=not (new_Node.player1Turn ^ hasNewScore))

        return new_Node

    def MiniMaxAlg(self,Node: State,depth: int = 0,max_depth: int = 0,alpha: float = -np.inf,beta: float = np.inf,) -> float:
        if time() >= self.totalTime:
            raise TimeoutError()

        if self.game_over(Node) or depth == max_depth:
            return self.utility_function(Node)

        if self.isPlayer1 == Node.player1Turn:
            value = -np.inf
            actions = self.successor_function(Node)
            for action in actions:
                value = max(value,self.MiniMaxAlg(self.new_State(Node, action),depth=depth + 1,max_depth=max_depth,alpha=alpha,beta=beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = np.inf
            actions = self.successor_function(Node)
            for action in actions:
                value = min(value,self.MiniMaxAlg(self.new_State(Node, action),depth=depth + 1,max_depth=max_depth,alpha=alpha,beta=beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    
    def game_over(self, Node: State) -> bool:
        return np.all(Node.rowStatus == 1) and np.all(Node.colStatus == 1)

   
    def utility_function(self, Node: State) -> float:

        [Ys, Xs] = Node.boardStatus.shape
        utility = 0


        won = 0
        lost = 0
        for y in range(Ys):
            for x in range(Xs):
                if self.isPlayer1:
                    if Node.boardStatus[y, x] == -4:
                        utility += 1
                        won += 1
                    elif Node.boardStatus[y, x] == 4:
                        utility -= 1
                        lost += 1
                else:
                    if Node.boardStatus[y, x] == -4:
                        utility -= 1
                        lost += 1
                    elif Node.boardStatus[y, x] == 4:
                        utility += 1
                        won += 1


        if self.long_chains_no(Node) % 2 == 0 and self.isPlayer1:
            utility += 1
        elif self.long_chains_no(Node) % 2 != 0 and not self.isPlayer1:
            utility += 1


        if won >= (self.n) ** 2 // 2 + 1:
            utility = np.inf
        elif lost >= (self.n) ** 2 // 2 + 1:
            utility = -np.inf

        return utility


    def long_chains_no(self, Node: State) -> int:

        long_chains_no = 0
        chains_list: List[List[int]] = []

        for box_num in range(((self.n)) ** 2):
            flag = False
            for chain in chains_list:
                if box_num in chain:
                    flag = True
                    break

            if not flag:
                chains_list.append([box_num])
                self.adjacent_boxes(Node, chains_list, box_num)

        for chain in chains_list:
            if len(chain) >= 3:
                long_chains_no += 1

        return long_chains_no

    # Find adjacent box(es) which can build chain
    def adjacent_boxes(self, Node: State, chains_list: List[List[int]], box_num):

        neighbors_num = [box_num - 1, box_num - (self.n), box_num + 1, box_num + (self.n)]

        for index in range(len(neighbors_num)):
            if (neighbors_num[index] < 0 or neighbors_num[index] > (self.n) ** 2 - 1
                    or (index % 2 == 0 and neighbors_num[index] // (self.n) != box_num // (self.n))):
                continue

            flag = False
            for chain in chains_list:
                if neighbors_num[index] in chain:
                    flag = True
                    break

            if not flag and index % 2 == 0:
                box = max(box_num, neighbors_num[index])
                if not Node.colStatus[box // (self.n)][box % (self.n)]:
                    chains_list[-1].append(neighbors_num[index])
                    self.adjacent_boxes(Node, chains_list, neighbors_num[index])

            if not flag and index % 2 != 0:
                box = max(box_num, neighbors_num[index])
                if not Node.rowStatus[box // (self.n)][box % (self.n)]:
                    chains_list[-1].append(neighbors_num[index])
                    self.adjacent_boxes(Node, chains_list, neighbors_num[index])
=======
from time import time
from Action import Action
from State import State
from typing import List
import numpy as np

Late = 0.5


class AIBot():

    
    def __init__(self, dots: int):
        self.isPlayer1 = True
        self.totalTime = 0
        self.n = dots - 1

   # == transition model == #
    def transitionModel(self, Node: State) -> Action:

        self.isPlayer1 = Node.player1Turn
        BestAction = None
        self.totalTime = time() + Late

        EmptyRows = np.count_nonzero(Node.rowStatus == 0)
        EmptyColumns = np.count_nonzero(Node.colStatus == 0)
        
        for depth in range(EmptyRows + EmptyColumns):
            try:
                # all child of node
                actions = self.successor_function(Node)
                utilities = np.array(
                    [self.MiniMaxAlg(self.new_State(Node, action), max_depth=depth + 1) for action in actions])
                index = np.random.choice(np.flatnonzero(utilities == utilities.max()))
                BestAction = actions[index]

            except TimeoutError:
                break
       
        return BestAction

    
    def successor_function(self, Node: State) -> List[Action]:
        rows = self.validPositions(Node.rowStatus)
        cols = self.validPositions(Node.colStatus)
        actions: List[Action] = []

        for Position in rows:
            actions.append(Action("row", Position))
        for Position in cols:
            actions.append(Action("col", Position))

        return actions

    
    def validPositions(self, Array: np.ndarray):
        [Ys, Xs] = Array.shape
        ValidPos: List[tuple[int, int]] = []

        for y in range(Ys):
            for x in range(Xs):
                if Array[y, x] == 0:
                    ValidPos.append((x, y))

        return ValidPos

    # == Update board
    def new_State(self, Node: State, newActon: Action) -> State:
        type = newActon.Type
        x, y = newActon.Position

        new_Node = State(
            Node.boardStatus.copy(),
            Node.rowStatus.copy(),
            Node.colStatus.copy(),
            Node.player1Turn,
        )

        player_flag = -1 if new_Node.player1Turn else 1

        hasNewScore = False
        point = 1

        [Ys, Xs] = new_Node.boardStatus.shape


        if y < Ys and x < Xs:
            new_Node.boardStatus[y, x] = (abs(new_Node.boardStatus[y, x]) + point) * player_flag
            if abs(new_Node.boardStatus[y, x]) == 4:
                hasNewScore = True


        if type == "row":
            new_Node.rowStatus[y, x] = 1
            if y > 0:
                new_Node.boardStatus[y - 1, x] = (abs(new_Node.boardStatus[y - 1, x]) + point) * player_flag
                if abs(new_Node.boardStatus[y - 1, x]) == 4:
                    hasNewScore = True


        elif type == "col":
            new_Node.colStatus[y, x] = 1
            if x > 0:
                new_Node.boardStatus[y, x - 1] = (abs(new_Node.boardStatus[y, x - 1]) + point) * player_flag
                if abs(new_Node.boardStatus[y, x - 1]) == 4:
                    hasNewScore = True

        new_Node = new_Node._replace(player1Turn=not (new_Node.player1Turn ^ hasNewScore))

        return new_Node

    def MiniMaxAlg(self,Node: State,depth: int = 0,max_depth: int = 0,alpha: float = -np.inf,beta: float = np.inf,) -> float:
        if time() >= self.totalTime:
            raise TimeoutError()

        if self.game_over(Node) or depth == max_depth:
            return self.utility_function(Node)

        if self.isPlayer1 == Node.player1Turn:
            value = -np.inf
            actions = self.successor_function(Node)
            for action in actions:
                value = max(value,self.MiniMaxAlg(self.new_State(Node, action),depth=depth + 1,max_depth=max_depth,alpha=alpha,beta=beta))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = np.inf
            actions = self.successor_function(Node)
            for action in actions:
                value = min(value,self.MiniMaxAlg(self.new_State(Node, action),depth=depth + 1,max_depth=max_depth,alpha=alpha,beta=beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    
    def game_over(self, Node: State) -> bool:
        return np.all(Node.rowStatus == 1) and np.all(Node.colStatus == 1)

   
    def utility_function(self, Node: State) -> float:

        [Ys, Xs] = Node.boardStatus.shape
        utility = 0


        won = 0
        lost = 0
        for y in range(Ys):
            for x in range(Xs):
                if self.isPlayer1:
                    if Node.boardStatus[y, x] == -4:
                        utility += 1
                        won += 1
                    elif Node.boardStatus[y, x] == 4:
                        utility -= 1
                        lost += 1
                else:
                    if Node.boardStatus[y, x] == -4:
                        utility -= 1
                        lost += 1
                    elif Node.boardStatus[y, x] == 4:
                        utility += 1
                        won += 1


        if self.long_chains_no(Node) % 2 == 0 and self.isPlayer1:
            utility += 1
        elif self.long_chains_no(Node) % 2 != 0 and not self.isPlayer1:
            utility += 1


        if won >= (self.n) ** 2 // 2 + 1:
            utility = np.inf
        elif lost >= (self.n) ** 2 // 2 + 1:
            utility = -np.inf

        return utility


    def long_chains_no(self, Node: State) -> int:

        long_chains_no = 0
        chains_list: List[List[int]] = []

        for box_num in range(((self.n)) ** 2):
            flag = False
            for chain in chains_list:
                if box_num in chain:
                    flag = True
                    break

            if not flag:
                chains_list.append([box_num])
                self.adjacent_boxes(Node, chains_list, box_num)

        for chain in chains_list:
            if len(chain) >= 3:
                long_chains_no += 1

        return long_chains_no

    # Find adjacent box(es) which can build chain
    def adjacent_boxes(self, Node: State, chains_list: List[List[int]], box_num):

        neighbors_num = [box_num - 1, box_num - (self.n), box_num + 1, box_num + (self.n)]

        for index in range(len(neighbors_num)):
            if (neighbors_num[index] < 0 or neighbors_num[index] > (self.n) ** 2 - 1
                    or (index % 2 == 0 and neighbors_num[index] // (self.n) != box_num // (self.n))):
                continue

            flag = False
            for chain in chains_list:
                if neighbors_num[index] in chain:
                    flag = True
                    break

            if not flag and index % 2 == 0:
                box = max(box_num, neighbors_num[index])
                if not Node.colStatus[box // (self.n)][box % (self.n)]:
                    chains_list[-1].append(neighbors_num[index])
                    self.adjacent_boxes(Node, chains_list, neighbors_num[index])

            if not flag and index % 2 != 0:
                box = max(box_num, neighbors_num[index])
                if not Node.rowStatus[box // (self.n)][box % (self.n)]:
                    chains_list[-1].append(neighbors_num[index])
                    self.adjacent_boxes(Node, chains_list, neighbors_num[index])
>>>>>>> f0a8fb5dfb2784b38af1cda5cd8726640744375b
