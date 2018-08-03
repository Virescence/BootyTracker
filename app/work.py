import difflib
import math

resource_dict = {1: "Chickens", 2: "Pigs", 3: "Snakes", 4: "Gunpowder"}
# cardinal_dict = {0: "N", 22.5: "NNW", 45: "NW", 67.5: "WNW", 90: "W", 112.5: "WSW", 135: "SW", 157.5: "SSW", 180: "S",
#                  202.5: "SSE", 225: "SE", 247.5: "ESE", 270: "E", 292.5: "ENE", 315: "NE", 337.5: "NNE", 360: "N"}

cardinal_dict = {0: "East", 22.5: "East by Northeast", 45: "Northeast", 67.5: "North by Northeast", 90: "North",
                 112.5: "North by Northwest", 135: "Northwest", 157.5: "West by Northwest", 180: "West",
                 202.5: "West by Southwest", 225: "Southwest", 247.5: "South by Southwest", 270: "South",
                 292.5: "South by Southeast", 315: "Southeast", 337.5: "East by Southeast", 360: "East"}

alphaNumeric = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, "k": 11, "l": 12,
                "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, "t": 20, "u": 21, "v": 22, "w": 23,
                "x": 24, "y": 25, "z": 26}

flippedY = {26: 1, 25: 2, 24: 3, 23: 4, 22: 5, 21: 6, 20: 7, 19: 8, 18: 9, 17: 10, 16: 11, 15: 12, 14: 13, 13: 14,
            12: 15, 11: 16, 10: 17, 9: 18, 8: 19, 7: 20, 6: 21, 5: 22, 4: 23, 3: 24, 2: 25, 1: 26}

island_dict = {}

island_list = []

message_list = []

class Island:
    def __init__(self, name, xCoord, yCoord, resources):
        self.name = name
        self.unchanged_coordinates = "(" + xCoord.strip() + ", " + yCoord.strip() + ")"
        self.coordinates = (alphaNumeric[xCoord.replace(" ", "").lower()], flippedY[int(yCoord.replace(" ", ""))])
        self.resources = [res.replace(" ", "") for res in resources]
        self.usefulResources = 0
        self.resourceWeight = 0
        self.midDistanceWeight = 0
        self.startDistanceWeight = 0
        self.totalWeight = 0
        island_dict[self.name] = self

    def calculateTotalWeight(self):
        self.totalWeight = self.midDistanceWeight + (self.usefulResources * -5) + self.startDistanceWeight

    def resetWeight(self):
        self.totalWeight = 0
        self.startDistanceWeight = 0
        self.midDistanceWeight = 0
        self.resourceWeight = 0
        self.usefulResources = 0

class Message:
    def __init__(self):
        self.step = ""
        self.cardinal = ""
        self.resources = ""
        self.next_stop = ""
        self.island_has_resource = False
        self.this_island_name = ""
        self.this_island_resources = ""
        self.coords = ""

def buildislandlist():

    # with open("resources.txt") as resourceFile:
        # rawIslandList = [line.strip('\n').replace('\t', "").split(",") for line in resourceFile if len(line) > 4]
        # print(rawIslandList)
    rawIslandList = [['Golden Sands Outpost', ' D', ' 12'], ['Sanctuary Outpost', ' G', ' 7'],
                     ['Plunder Outpost', ' M', ' 22'], ['Ancient Spire Outpost', ' V', ' 21'],
                     ["Galleon's Grave Outpost", ' X', ' 9'], ['Dagger Tooth Outpost', ' Q', ' 8'],
                     ['Keel Haul Fort', ' C', ' 7', 'Gunpowder'], ['Hidden Spring Keep', ' K', ' 9', 'Gunpowder'],
                     ["Sailor's Knot Stronghold", ' E', ' 17', 'Gunpowder'], ['Lost Gold Fort', ' J', ' 21', 'Gunpowder'],
                     ['Old Boot Fort', ' P', ' 17', 'Gunpowder'], ["The Crow's Nest Fortress", ' S', ' 22', 'Gunpowder'],
                     ['Shark Fin Camp', ' U', ' 5', 'Gunpowder'], ['Kraken Watchtower', ' O', ' 6', 'Gunpowder'], ['Skull Keep', ' U', ' 11', 'Gunpowder'],
                     ['Barnacle Cay', ' T', ' 19', ' Chickens'], ['Black Sand Atoll', ' T', ' 3', ' Snakes'],
                     ['Black Water Enclave', ' X', ' 5', ' Chickens'], ["Blind Man's Lagoon", ' S', ' 6', ' Pigs'],
                     ['Booty Island', ' N', ' 25', ' Snakes'], ['Boulder Cay', ' H', ' 5', ' Pigs'],
                     ['Cannon Cove', ' H', ' 11', ' Pigs', 'Chickens'], ['Castaway Isle', ' M', ' 16', ' Snakes'],
                     ['Chicken Isle', ' K', ' 19', ' Chickens'], ['Crescent Isle', ' B', ' 10', ' Pigs', ' Snakes'],
                     ["Crook's Hollow", ' Q', ' 19', ' Chickens', ' Snakes'], ['Cutlass Cay', ' Q', ' 22', 'Snakes'],
                     ["Devil's Ridge", ' U', ' 24', ' Pigs', ' Snakes'],
                     ['Discovery Ridge', ' E', ' 21', ' Chickens', ' Snakes'], ['Fools Lagoon', ' K', ' 17', ' Pigs'],
                     ['Isle of Last Words', ' S', ' 10', ' Snakes'], ["Kraken's Fall", ' X', ' 15', ' Pigs', ' Snakes'],
                     ['Lagoon of Whispers', ' D', ' 15', 'Snakes'], ["Liar's Backbone", ' Y', ' 13', 'Snakes'],
                     ['Lone Cove', ' J', ' 6', ' Pigs', ' Snakes'], ['Lonely Isle', ' I', ' 9', ' Snakes'],
                     ['Lookout Point', ' L', ' 25', ' Pigs'], ["Marauder's Arch", ' V', ' 3', ' Chickens', ' Snakes'],
                     ["Mermaid's Hideaway", ' B', ' 16', ' Chickens', ' Pigs'],
                     ['Mutineer Rock', ' R', ' 24', ' Chickens', ' Pigs'],
                     ['Old Faithful isle', ' Q', ' 4', ' Chickens', ' Pigs'],
                     ['Old Salts Atoll', ' G', ' 23', ' Chickens'], ['Paradise Spring', ' O', ' 21', ' Pigs'],
                     ['Picaroon Palms', ' K', ' 4', ' Snakes'], ["Plunderer's Plight", ' V', ' 6', ' Pigs'],
                     ['Plunder Valley', ' H', ' 19', ' Chicken', ' Pigs'], ['Rapier Cay', ' D', ' 9', ' Chickens'],
                     ['Rum Runner Isle', ' J', ' 11', 'Pigs'], ["Sailer's Bounty", 'B', '4', ' Chickens', ' Pigs'],
                     ['Salty Sands', ' I', ' 3', ' Chickens'], ['Sandy Shallows', ' E', ' 5', ' Snakes'],
                     ['Scurvy Island', ' N', ' 4', ' Chickens'], ["Sea Dog's Rest", ' B', ' 13', ' Chickens', ' Pigs'],
                     ['Shark Bait Cove', ' I', ' 24', ' Chickens', ' Pigs'], ['Shark Tooth Key', ' U', ' 15', 'Pigs'],
                     ['Shipwreck Bay', ' Q', ' 12', ' Chickens', ' Pigs'], ['Shiver Retreat', ' V', ' 13', ' Pigs'],
                     ["Smuggler's Bay", ' F', '3', ' Chickens', ' Snakes'],
                     ['Snake Island', ' N', ' 19', ' Pigs', ' Snakes'],
                     ['The Crooked Masts', ' T', ' 13', ' Chickens', ' Snakes'],
                     ['The Sunken Grove', ' T', ' 8', 'Pigs', ' Snakes'],
                     ["Thieve's Haven", ' P', ' 25', ' Chickens', ' Pigs'], ['Tri-Rock Isle', ' W', ' 11', ' Chickens'],
                     ['Twin Groves', ' I', ' 13', ' Chickens'],
                     ['Wanderers Refuge', ' G', ' 15', ' Chickens', ' Snakes']]

    for x in rawIslandList:
        island_list.append(Island(x[0], x[1], x[2], x[3:]))

    return island_list

def getIslandList():
    if len(island_list) == 0:
        return buildislandlist()
    else:
        return island_list

def gatherInput(islandList):
    needs_curr_pos = True
    needs_destination = True
    needs_resource = True
    current_position = ""
    destination = ""
    resources_list = []

    while needs_curr_pos:
        current_position = input("To start your adventure, enter you current location here: " + "\n").lower()
        try:
            interpreted_current_position = difflib.get_close_matches(current_position, [island.name for island in islandList])[0]
            print("You are at: " + interpreted_current_position + "\n")
            needs_curr_pos = False
        except:
            print("Invalid starting position")

    while needs_destination:
        destination = input("Where do you need to deliver to? \n").lower()
        try:
            interpreted_destination = difflib.get_close_matches(destination, [island.name for island in islandList])[0]
            print("Your destination is: " + interpreted_destination + "\n")
            needs_destination = False
        except:
            print("Invalid destination")

    while needs_resource:
        needed_resources = input("What do you need? (Chickens (1), Pigs(2), Snakes(3), Gunpowder(4))\n")
        resources_list_raw = [int(x) for x in needed_resources if x.isdigit() and x not in resources_list]
        resources_list = []
        [resources_list.append(resource_dict[x]) for x in resources_list_raw if x not in resources_list]

        if any(resources_list):
            needs_resource = False
            # for x in resources_list:
                # print("You need: %s" % x)

        else:
            print("please enter numbers corresponding with a resource")
    print("************************")
    return interpreted_current_position, interpreted_destination, resources_list

def angleMath(startPos, endPos):
    startX = startPos[0]
    startY = startPos[1]

    endX = endPos[0]
    endY = endPos[1]


    if endX > startX and endY == startY:
        deg = 0
        return cardinal_dict[min(cardinal_dict, key=lambda x:abs(x-deg))]

    elif endX == startX and endY > startY:
        deg = 90
        return cardinal_dict[min(cardinal_dict, key=lambda x:abs(x-deg))]

    elif endX < startX and endY == startY:
        deg = 180
        return cardinal_dict[min(cardinal_dict, key=lambda x:abs(x-deg))]

    elif endX == startX and endY < startY:
        deg = 270
        return cardinal_dict[min(cardinal_dict, key=lambda x:abs(x-deg))]

    deg = math.degrees((math.atan(math.fabs(startY - endY) / math.fabs(startX - endX))))

    if endX < startX and endY > startY:
        deg = 180 - deg

    elif endX < startX and endY < startY:
        deg = deg + 180

    elif endX > startX and endY < startY:
        deg = 360 - deg

    return cardinal_dict[min(cardinal_dict, key=lambda x:abs(x-deg))]

def navigateNoResources(start_name, destination_name):

    # s = "%s is %s from you" % (destination_name, direction)
    s = Message()
    s.cardinal = direction = angleMath(island_dict[start_name].coordinates, island_dict[destination_name].coordinates)
    s.next_stop = destination_name
    return [s]

def getDistanceList(start, destination, mid=True):
    if mid:
        reference_point = (((start.coordinates[0] + destination.coordinates[0])/2),
                           ((start.coordinates[1] + destination.coordinates[1])/2))
    else:
        reference_point = start.coordinates

    distanceList = []

    for island in island_list:
        distance = math.sqrt((island.coordinates[0] - reference_point[0]) ** 2 +
                             (island.coordinates[1] - reference_point[1]) ** 2)

        distanceList.append((distance, island))


    distanceList.sort(key=lambda x: x[0])

    return [x[1] for x in distanceList]

def resetWeights():
    [x.resetWeight() for x in island_list]

def test():
    a = Message()
    b = Message()
    a.next_stop = "alol"
    b.next_stop = "b lol"
    message_list.append(a)
    message_list.append(b)
    print("lol")
    return message_list
    # buildislandlist()
    # getDistanceList(island_dict["Booty Island"], island_dict["Rapier Cay"])

def navigate(start_name, destination_name, needed_resources, message=None):
        if message == None:
            message = []
        step_message = Message()
        if len(message) == 0:
            step_message.step = "First Stop"
        else:
            step_message.step = "Next Stop"
        # print(needed_resources)
        # print("length of island list: " + str(len(island_list)))
        resetWeights()
        start, destination = island_dict[start_name], island_dict[destination_name]
        mid_distance_list = getDistanceList(start, destination, mid=True)
        start_distance_list = getDistanceList(start, destination, mid=False)

        # Reset and calculate new resource weight for each island
        for island in mid_distance_list:
            island.usefulResources = 0
            for resource in needed_resources:
                if resource in island.resources:
                    island.usefulResources += 1


        # Create a list and sort with islands with most "needed_resources" at top
        # Trim lists of anything that has no "needed_resources"
        start_distance_list = [x for x in start_distance_list if x.usefulResources > 0]
        mid_distance_list = [x for x in mid_distance_list if x.usefulResources > 0]
        res_weighted_list = [x for x in mid_distance_list if x.usefulResources > 0]
        res_weighted_list.sort(key=lambda x: x.usefulResources, reverse=True)
        # [print(x.name, x.usefulResources) for x in res_weighted_list]


        for island in mid_distance_list:
            island.midDistanceWeight = mid_distance_list.index(island)
            # print("MID DISTNACE LIST: " + island.name + " " + str(island.midDistanceWeight))

        for island in start_distance_list:
            island.startDistanceWeight = start_distance_list.index(island)
            # print("START DISTNACE LIST: " + island.name + " " + str(island.startDistanceWeight))

        # [print("RESOURCE LIST: " + island.name + " " + str(island.usefulResources)) for island in res_weighted_list]

        for island in res_weighted_list:
            island.resourceWeight = res_weighted_list.index(island)
            island.calculateTotalWeight()
            # print("TOTAL WEIGHT: " + island.name + " " + str(island.totalWeight))



        res_weighted_list.sort(key=lambda x: x.totalWeight)

        if start != res_weighted_list[0]:
            next_stop = res_weighted_list[0]
        else:
            # This should only happen when the starting island is an island that has a needed resource
            step_message.island_has_resource = True
            step_message.this_island_name = start_name
            step_message.this_island_resources = resourceStringBuilder(start.resources)
            next_stop = res_weighted_list[1]

        step_message.next_stop = next_stop.name
        step_message.resources = resourceStringBuilder(next_stop.resources)
        step_message.coords = str(next_stop.unchanged_coordinates)

        if start != destination:
            step_message.cardinal = angleMath(start.coordinates, next_stop.coordinates)


        if len(needed_resources) > 0:
            for res in next_stop.resources:
                if res in needed_resources:
                    needed_resources.remove(res)

            if len(needed_resources) > 0:
                message.append(step_message)
                navigate(next_stop.name, destination.name, needed_resources, message)

            else:
                message.append(step_message)
                step_message = Message()
                step_message.next_stop = destination.name
                step_message.step = "Final Destination"
                step_message.coords = str(destination.unchanged_coordinates)
                message.append(step_message)
                if next_stop.coordinates != destination.coordinates:
                    step_message.cardinal = angleMath(next_stop.coordinates, destination.coordinates)

        return message

def trash():
    print("1")
    return

def main():

    resetWeights()
    islandList = buildislandlist()

    while True:
        workTuple = gatherInput(islandList)
        startName = workTuple[0]
        destinationName = workTuple[1]
        resources = workTuple[2]
        navigate(startName, destinationName, resources)

def resourceStringBuilder(resources):
    if len(resources) == 1:
        return resources[0]

    if len(resources) == 2:
        return resources[0] + " and " + resources[1]

    if len(resources) > 2:
        res_string = ""
        for res in resources[:-1]:
            res_string += res + ", "
        res_string += "and " + resources[-1]
        return res_string

def determineResources(pig, chicken, snake, gunpowder):
    needed_resources = []
    if pig:
        needed_resources.append("Pigs")
    if chicken:
        needed_resources.append("Chickens")
    if snake:
        needed_resources.append("Snakes")
    if gunpowder:
        needed_resources.append("Gunpowder")

    return needed_resources


# if __name__ == "__main__":
    # print(os.environ.get('SECRET_KEY') or 'idkfa')
    # main()
    # test()
