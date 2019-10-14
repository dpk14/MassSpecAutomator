#return string format: volts, current, reistance, time, status

FIELD_NAMES = ["volts", "current", "resistance", "time", "status"]
NUM_FIELDS = len(FIELD_NAMES)

#this method translates the return string into a dict of field names mapped to arrays of readings

def translate(result):
    print(result)
    result = result.split(",")
    result = remove_junk_characters(result)
    map = initialize_map()
    for index in range(len(result)):
        starting_index = int(index*NUM_FIELDS)
        if starting_index >= len(result):
            break
        for field_index in range(NUM_FIELDS):
            field_name = FIELD_NAMES[field_index]
            actual_index = starting_index + field_index
            reading = result[actual_index]
            map[field_name].append(reading)
    print(map)
    return map

def initialize_map():
    map = {}
    for name in FIELD_NAMES:
        map[name] = []
    return map

def remove_junk_characters(result):
    end_index = len(result) - 1
    cleaned_end = result[end_index].replace("\n", "")
    result[end_index] = cleaned_end
    return result 