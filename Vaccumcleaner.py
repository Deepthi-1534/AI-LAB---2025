from typing import Set, Tuple

class Robot:
    def move(self) -> bool:
        """Moves the robot forward by one unit in the current direction."""
        raise NotImplementedError
    
    def turnLeft(self) -> None:
        """Turns the robot 90 degrees to the left."""
        raise NotImplementedError
    
    def turnRight(self) -> None:
        """Turns the robot 90 degrees to the right."""
        raise NotImplementedError
    
    def clean(self) -> None:
        """Cleans the current cell."""
        raise NotImplementedError


class RobotCleaner:
    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def __init__(self):
        self.visited: Set[Tuple[int, int]] = set()
        self.robot = None
    
    def cleanRoom(self, robot: Robot):
        self.robot = robot
        self.dfs(0, 0, 0)
    
    def dfs(self, row: int, col: int, direction: int):
        self.robot.clean()
        self.visited.add((row, col))
        
        for k in range(4):
            new_direction = (direction + k) % 4
            dr, dc = self.directions[new_direction]
            new_row, new_col = row + dr, col + dc
            
            if (new_row, new_col) not in self.visited and self.robot.move():
                self.dfs(new_row, new_col, new_direction)
                
                # Backtrack: turn 180 degrees, move back, then turn 180 degrees again
                self.robot.turnRight()
                self.robot.turnRight()
                self.robot.move()
                self.robot.turnRight()
                self.robot.turnRight()
            
            self.robot.turnRight()


class MockRobot(Robot):
    def __init__(self):
        # 1 = open space, 0 = obstacle
        self.room = [
            [1,1,1,1,0],
            [1,0,1,0,1],
            [1,1,1,1,1],
            [0,1,0,1,0],
            [1,1,1,1,1]
        ]
        self.row = 0
        self.col = 0
        self.direction = 0  # 0=up,1=right,2=down,3=left
        
        # Directions match the RobotCleaner directions order
        self.directions = [(-1,0),(0,1),(1,0),(0,-1)]
    
    def move(self) -> bool:
        dr, dc = self.directions[self.direction]
        new_row, new_col = self.row + dr, self.col + dc
        
        if 0 <= new_row < len(self.room) and 0 <= new_col < len(self.room[0]) and self.room[new_row][new_col] == 1:
            self.row, self.col = new_row, new_col
            # Reduced output: no print here
            return True
        return False
    
    def turnLeft(self) -> None:
        self.direction = (self.direction - 1) % 4
        # Reduced output: no print here
    
    def turnRight(self) -> None:
        self.direction = (self.direction + 1) % 4
        # Reduced output: no print here
    
    def clean(self) -> None:
        print(f"Cleaned cell ({self.row}, {self.col})")


if __name__ == "__main__":
    robot = MockRobot()
    cleaner = RobotCleaner()
    cleaner.cleanRoom(robot)
