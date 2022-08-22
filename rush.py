from heapq import heappush, heappop
class Car:
    def __init__(self, i, j, L, horiz):
        """
        Parameters
        i: int
            Row of the car
        j: int
            Column of the car
        L: int
            Length of the car
        horiz: boolean
            True if the car is horizontal, false
            if the car is vertical
        """
        self.i = i
        self.j = j
        self.L = L
        self.horiz = horiz

class State:
    def __init__(self):
        self.N = 0 # Our cars are on an NxN grid
        self.cars = [] # The first car is the red car
        self.goal = [0, 0] # The state that our red car needs to reach
        self.prev = None # Pointers to previous states (use later)

    def clone(self):
        """
        Make a deep copy of this state

        Return
        ------
        State: Deep copy of this state
        """
        s = State()
        s.N = self.N
        for c in self.cars:
            s.cars.append(Car(c.i, c.j, c.L, c.horiz))
        s.goal = self.goal.copy()
        return s

    def load_puzzle(self, filename):
        """
        Load in a puzzle from a text file
        
        Parameters
        ----------
        filename: string
            Path to puzzle
        """
        fin = open(filename)
        lines = fin.readlines()
        fin.close()
        self.N = int(lines[0])
        self.goal = [int(k) for k in lines[1].split()]
        for line in lines[2::]:
            fields = line.rstrip().split()
            i, j, L = int(fields[0]), int(fields[1]), int(fields[3])
            horiz = True
            if "v" in fields[2]:
                horiz = False
            self.cars.append(Car(i, j, L, horiz))

    def get_state_grid(self):
        """
        Return an NxN 2D list corresponding to this state.  Each
        element has a number corresponding to the car that occupies 
        that cell, or is a -1 if the cell is empty

        Returns
        -------
        list of list: The grid of numbers for the state
        """
        grid = [[-1]*self.N for i in range(self.N)]
        for idx, c in enumerate(self.cars):
            di = 0
            dj = 0
            if c.horiz:
                dj = 1
            else:
                di = 1
            i, j = c.i, c.j
            for k in range(c.L):
                grid[i][j] = idx
                i += di
                j += dj
        return grid
    
    def __str__(self):
        """
        Get a string representing the state

        Returns
        -------
        string: A string representation of this state
        """
        s = ""
        grid = self.get_state_grid()
        for i in range(self.N):
            for j in range(self.N):
                s += "%5s"%grid[i][j]
            s += "\n"
        return s
    
    def __lt__(self, other):
        """
        Overload the less than operator so that ties can
        be broken automatically in a heap without crashing

        Parameters
        ----------
        other: State
            Another state
        
        Returns
        -------
        Result of < on string comparison of __str__ from self
        and other
        """
        return str(self) < str(other)
    
    def get_state_hashable(self):
        """
        Return a shorter string without line breaks that can be
        used to hash the state

        Returns
        -------
        string: A string representation of this state
        """
        s = ""
        grid = self.get_state_grid()
        for i in range(self.N):
            for j in range(self.N):
                s += "{}".format(grid[i][j])
        return s

    def plot(self):
        """
        Create a new figure and plot the state of this puzzle,
        coloring the cars by different colors
        """
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib.colors import ListedColormap
        c = cm.get_cmap("Paired", len(self.cars))
        colors = [[1, 1, 1, 1], [1, 0, 0, 1]]
        colors = colors + c.colors.tolist()
        cmap = ListedColormap(colors)
        grid = self.get_state_grid()
        grid = np.array(grid)
        plt.imshow(grid, interpolation='none', cmap=cmap)
        
    def is_goal(self):
        """
        Determines the first car and checks to see if the square all the way to the right is equal to the goal.
        """
        grid = self.get_state_grid()
        first_car= self.cars[0]
        
        if [first_car.j + first_car.L - 1] == [self.goal[1]]:
            Goal = True
        else:
            Goal = False
        return Goal
    
    def get_neighbors(self):
        '''
        Checks below, above, right and left of cars to see if there is an open space. 
        If there is, it clones the board, moves the car and appends it to the neighbors array
        '''
        grid = self.get_state_grid()
        neighbors= []
        for i in range(len(self.cars)):
            #Loops through all possible cars
            state = self.clone()
            vehicle = state.cars[i]
           
                       
            if vehicle.horiz:
                #Establishes the cordinate that is the furthest right for the car
                rightmost_square = vehicle.j + (vehicle.L - 1)
                
                 #Checks to make sure the square is not on the right border of the grid. 
                 #Checks to see if there is an open spot to the right of the car
                
                if rightmost_square < len(grid) - 1:
                    if grid[vehicle.i][rightmost_square + 1] == -1:
                        cloned_board = self.clone() 
                        current_car = i
                        cloned_board.move_right(current_car)
                        neighbors.append(cloned_board)
                
                #Checks to make sure the car is not on left border of the grid
                #Checks to see if there is an open spot to the left of the car
                
                if vehicle.j >= 1:
                    if grid[vehicle.i][vehicle.j - 1] == -1:
                        cloned_board = self.clone() 
                        current_car = i
                        cloned_board.move_left(current_car)
                        neighbors.append(cloned_board)
           
            else:
                #Establishes the cordinate that is the lowest for the car
                lowest_square = vehicle.i + (vehicle.L - 1)
                
                #Checks to make sure the car is not on the bottom border of the grid. 
                #Checks to see if there is an open spot below the car
                
                if lowest_square < len(grid) - 1:
                    if grid[lowest_square + 1][vehicle.j] == -1:
                        cloned_board = self.clone() 
                        current_car = i
                        cloned_board.move_up(current_car)
                        neighbors.append(cloned_board)
                        
                #Checks to make sure the car is not on the top border of the grid. 
                #Checks to see if there is an open spot above the car
                        
                if vehicle.i >= 1:
                    if grid[vehicle.i - 1][vehicle.j] == -1:
                        cloned_board = self.clone() 
                        current_car = i
                        cloned_board.move_down(current_car)
                        neighbors.append(cloned_board)
                        
        return neighbors
    
    #Method to move the car to the right
    def move_right(self, current_car):
        self.cars[current_car].j = self.cars[current_car].j + 1

    #Method to move the car to the left
    def move_left(self, current_car):
        self.cars[current_car].j = self.cars[current_car].j - 1
        
    #Method to move the car up    
    def move_up(self, current_car):
        self.cars[current_car].i = self.cars[current_car].i + 1
    
    #Method to move the car down
    def move_down(self,current_car):
        self.cars[current_car].i = self.cars[current_car].i -1
        
        
    def solve(self):
        '''
        This method gets the neighbors and adds the possible moves to the queue. The queue then pops off the values from the left
        and checks to see if they are equal to the goal. We reverse the list to show the solution from the beginning
        '''
        queue = [self] 
        finished = False
        end = None
        while len(queue) > 0 and not finished:
            state = queue.pop(0) #this makes it so the first element goes from the left
            if state.is_goal():
                end = state
                finished = True
            else:
                neighbs = state.get_neighbors()
                for move in neighbs:
                        move.prev = state
                        queue.append(move)
        states = [end]
        state = end
        while state.prev:
            state = state.prev
            states.append(state)
        states.reverse()
        return states
        pass
    
    def solve_graph(self):
        '''
        Peforms similarly solve but remembers where we previously visited in order to maximize the efficiency
        '''
        visited = set([])
        expanded = 1
        queue = [self] 
        finished = False
        end = None
        node = 0
        while len(queue) > 0 and not finished:
            expanded += 1
            state = queue.pop(0) 
            if state.is_goal():
                end = state
                finished = True
            else:
                neighbs = state.get_neighbors()
                for move in neighbs:
                    if not str(move) in visited:
                        move.prev = state
                        expanded += 1
                        queue.append(move)
                        visited.add(str(move)) 
                        node += 1  
        print(node)
        states = [end]
        state = end
        while state.prev:
            state = state.prev
            states.append(state)
        states.reverse()
        return states
    
    def heuristic(self):
        '''
        Creates a heurisitic where we check to see if the block is at the goal. If not we loop through the row. 
        If there are no cars, then the h_value is 1. If there is any car blocking its path, then the h_value is 2
        '''
        rightmost_square = self.cars[0].j + (self.cars[0].L - 1)
        grid = self.get_state_grid()
        h_value = 0  
        if self.is_goal():
            h_value = 0
        else: 
            h_value = 1
            for m in range (len(grid) - (rightmost_square + self.cars[0].j)):               
                if grid[self.cars[0].i][rightmost_square + m] == -1:
                    h_value = 1
                    
                if grid[self.cars[0].i][rightmost_square + m] != -1:
                    h_value = 2
                    break
               
        return h_value

    def original_heuristic(self):
        '''
        Created my own heuristic where we determine the distance between the car and the goal as well as the number of cars
        blocking it's path
        '''
        rightmost_square = self.cars[0].j + (self.cars[0].L - 1)
        grid = self.get_state_grid()
        goal = self.goal[1]
        numberOfCars = 0
        
        for m in range (len(grid) - (rightmost_square + self.cars[0].j)):      
            if grid[self.cars[0].i][rightmost_square + m] != -1:
                numberOfCars += 1
          
        return (goal - rightmost_square) + numberOfCars
        

    
    def solve_astar(self):    
        '''
        Through this code, we prioritize the cumulative cost and the heuristic to search more efficiently. By using  heappush and heappop 
        we are able to add more values to the queue. We also keep track of our previous moves like in the graph search
        '''
        frontier = []
        cumucost = 0
        d = 1
        costn = cumucost + self.heuristic()
        heappush(frontier, (costn, self, None, cumucost + d))
        visited = set([])                     
        reachedGoal = False
        end = None
        nodes = 0
        
        
        while not reachedGoal and len(frontier) > 0:
            (est, state, prev, cumucost) = heappop(frontier)
                                           
            if state.is_goal():
                reachedGoal = True
                end = state
                
            else:
                neighbors = state.get_neighbors()
                
                
                for n in neighbors:
                    if not n.get_state_hashable() in visited:  
                        n.prev = state
                        costn = cumucost + d + n.heuristic()
                        heappush(frontier, (costn, n, state, cumucost + d))
                        visited.add(n.get_state_hashable())    
                        nodes += 1                                       
                        
        print(nodes)
        
        states = [end]
        state = end
        while state.prev:
            state = state.prev
            states.append(state)  
            
        states.reverse()
        
        return states
        pass
        
    def solve_original_astar(self):   
        '''
        Utilizes my own heurisitc to run the A star method
        '''
        frontier = []
        cumucost = 0
        d = 1
        costn = cumucost + self.original_heuristic()
        heappush(frontier, (costn, self, None, cumucost + d))
        visited = set([])                     
        reachedGoal = False
        end = None
        node = 0
        
        
        while not reachedGoal and len(frontier) > 0:
            (est, state, prev, cumucost) = heappop(frontier)
                                           
            if state.is_goal():
                reachedGoal = True
                end = state
                
            else:
                neighbors = state.get_neighbors()
                
                
                for n in neighbors:
                    if not n.get_state_hashable() in visited:  
                        n.prev = state
                        costn = cumucost + d + n.original_heuristic()
                        heappush(frontier, (costn, n, state, cumucost + d))
                        visited.add(n.get_state_hashable())    
                        node += 1                                       
                        
        print(node)
        states = [end]
        state = end
        while state.prev:
            state = state.prev
            states.append(state)  
            
        states.reverse()
        
        return states
        pass
        
