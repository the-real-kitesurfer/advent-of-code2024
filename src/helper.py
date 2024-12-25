DEBUG = True

def debug(msg):
    if DEBUG:
        print(msg)

def fetchData(day, realData):
    if realData:
        filename = "./resources/data/day" + str(day) + ".txt"    
    else:
        filename = "./resources/samples/sample" + str(day) + ".txt"

    with open(filename, 'r') as f:
        lines = f.readlines()
        listOfStrings=[]
        for i, line in enumerate(lines):
            listOfStrings.append(line[:-1])
    
    return listOfStrings