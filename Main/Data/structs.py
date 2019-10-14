INFINITY = 100000
GOOD_COLOR = "green"
TOLERABLE_COLOR = "orange"
UNSAFE_COLOR = "red"

class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

class Stat:
    def __init__(self, good_ranges=(Range(-INFINITY, INFINITY), ), tolerable_ranges=(), unsafe_ranges=()):
        self.good_ranges = good_ranges
        self.tolerable_ranges = tolerable_ranges
        self.unsafe_ranges = unsafe_ranges

    def in_range(self, ranges, value):
        for range in ranges:
           if range.min < float(value) < range.max:
               return True
        return False

    def get_display_color(self, value):
        if self.in_range(self.good_ranges, value=value):
            return GOOD_COLOR
        if self.in_range(self.tolerable_ranges, value=value):
            return TOLERABLE_COLOR
        if self.in_range(self.unsafe_ranges, value=value):
            return UNSAFE_COLOR
