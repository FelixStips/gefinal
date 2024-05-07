import random
from enum import StrEnum

class MarketType(StrEnum):
    SMALL = "small_market"
    LARGE = "large_market"

class PersonRole(StrEnum):
    EMPLOYER = "employer"
    WORKER = "worker"



def assign_property(participants, property_name, property_value=True):
    for p in participants:
        p.vars[property_name] = property_value

def split_list_by_lengths(input_list, lengths):
    random.shuffle(input_list)
    """Split a list into sublists of specified lengths"""
    # Check if the sum of lengths exceeds the input list length
    assert sum(lengths) <= len(input_list), "The sum of the lengths exceeds the input list length"

    # Splitting the list according to the specified lengths
    result = []
    start_index = 0
    for length in lengths:
        # Calculate the end index for the current sublist
        end_index = start_index + length
        # Append the sublist to the result
        result.append(input_list[start_index:end_index])
        # Update the start index for the next sublist
        start_index = end_index

    # Append the rest of the list if there are any elements left
    if start_index < len(input_list):
        result.append(input_list[start_index:])

    return result