# MIT 6.00.2x
# Problem Set 2
# Simulating robots

import ps2_visualize
import pylab
import math
import random

random.seed(9000)  # Comment this out to get random walks


def testRobotMovement(robot_type, room_type, delay=0.4):
    """
    Runs a simulation of a single robot of type robot_type in a 5x5 room.
    """
    room = room_type(5, 5)
    robot = robot_type(room, 1)
    anim = ps2_visualize.RobotVisualization(1, 5, 5, delay)
    while room.getNumCleanedTiles() / room.getNumTiles() < 1:
        robot.updatePositionAndClean()
        anim.update(room, [robot])
    anim.done()


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert width > 0
        assert type(width) == int
        assert height > 0
        assert type(height) == int

        self.width = width
        self.height = height
        # Line bellow broken to comply with pep8
        self.room = [[False for x in range(self.width)] for y in
                     range(self.height)]

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.room[math.floor(pos.getY())][math.floor(pos.getX())] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.room[n][m]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return sum([len(x) for x in self.room])

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum([x.count(True) for x in self.room])

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # Line bellow broken to comply with pep8
        return Position(random.randrange(0, self.width),
                        random.randrange(0, self.height))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.getX() < 0 or pos.getY() < 0:
            return False
        return (pos.getX() < self.width and pos.getY() < self.height)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        assert speed > 0 and type(speed) == float
        self.room = room
        self.speed = speed
        self.currentPosition = self.room.getRandomPosition()
        self.currentDirection = random.randrange(0, 360)
        self.room.cleanTileAtPosition(self.currentPosition)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.currentPosition

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.currentDirection

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.currentPosition = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.currentDirection = direction


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Line bellow broken to comply with pep8
        newPosition = self.currentPosition.getNewPosition(
                      self.currentDirection, self.speed
                      )
        if self.room.isPositionInRoom(newPosition):
            self.currentPosition = newPosition
            self.room.cleanTileAtPosition(self.currentPosition)
        else:
            self.currentDirection = random.randrange(0, 360)


# ##Uncomment the line bellow to see StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newDirection = self.currentDirection
        while newDirection == self.currentDirection:
            newDirection = random.randrange(0, 360)
        self.currentDirection = newDirection
        # Line bellow broken to comply with pep8
        newPosition = self.currentPosition.getNewPosition(
                      newDirection, self.speed
                      )
        if self.room.isPositionInRoom(newPosition):
            self.currentPosition = newPosition
            self.room.cleanTileAtPosition(self.currentPosition)


# ##Uncomment the line bellow to see StandardRobot in action
# testRobotMovement(RandomWalkRobot, RectangularRoom)


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)

    returns: Cleaning time in timesteps
    """
    assert num_robots > 0 and type(num_robots) == int
    assert speed > 0 and type(speed) == float
    assert width > 0 and type(width) == int
    assert height > 0 and type(height) == int
    # Line bellow broken to comply with pep8
    assert (min_coverage >= 0 and min_coverage <=
            1.0 and type(min_coverage) == float)
    assert num_trials > 0 and type(num_trials) == int
    listOfNumberOfTimeSteps = []
    for i in range(num_trials):
        # ## Optional visualization
        # anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        # ## End of optional visualization
        numberOfTimeSteps = 0
        room = RectangularRoom(width, height)
        currentCoverage = 0
        robot = []
        for i in range(num_robots):
            robot.append(robot_type(room, speed))
        while currentCoverage < min_coverage:
            # ## Optional visualization
            # anim.update(room, robot)
            # ## End of optional visualization
            for i in robot:
                i.updatePositionAndClean()
            currentCoverage = room.getNumCleanedTiles() / room.getNumTiles()
            numberOfTimeSteps += 1
        listOfNumberOfTimeSteps.append(numberOfTimeSteps)
        # ## Optional visualization
        # anim.done()
        # ## End of optional visualization
    return float(sum(listOfNumberOfTimeSteps) / num_trials)


# ##Uncomment these lines bellow to see a simulation of how many time steps
# ##each implementation takes on average

# print('RandomWalkRobot cleaning time (in timesteps): ',
    #   round(runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot)))
# print('StandardRobot cleaning time (in timesteps): ',
#       round(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)))
