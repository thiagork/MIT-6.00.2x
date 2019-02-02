# MIT 6.00.2x
# Problem Set 1
# Transporting Cows Across Space


from ps1_partition import get_partitions
import time


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as
    values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = dict()
    f = open(filename, 'r')
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows.
    The returned allocation of cows may or may not be optimal.
    The greedy heuristic follows the following method:

    1. As long as the current trip can fit another cow, add the largest cow
    that will fit to the trip.
    2. Once the trip is full, begin a new trip to transport the remaining cows.

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cowsLeft = dict(cows)
    result = []
    while cowsLeft != {}:
        trip = []
        totalWeight = 0
        for i in sorted(cowsLeft, key=cowsLeft.get)[::-1]:
            if (totalWeight + cowsLeft[i]) <= limit:
                trip.append(i)
                totalWeight += cowsLeft[i]
                del cowsLeft[i]
        result.append(trip)
    return result


def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm follows the following method:

    1. Enumerate all possible ways that the cows can be divided into separate
    trips.
    2. Select the allocation that minimizes the number of trips without making
    any trip that does not obey the weight limitation.

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    listCows = list(get_partitions(cows))
    numberOfTrips = len(cows.keys()) + 1
    result = []
    for i in range(len(listCows)):
        if len(listCows[i]) < numberOfTrips:
            for j in range(len(listCows[i])):
                totalWeight = 0
                weightExceeded = False
                for k in listCows[i][j]:
                    totalWeight += cows[k]
                    if totalWeight > limit:
                        weightExceeded = True
                        break
                if weightExceeded:
                    break
            if not weightExceeded:
                numberOfTrips = len(listCows[i])
                result = list(listCows[i])
    return result


cows = load_cows("ps1_cow_data.txt")
limit = 15


print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))
