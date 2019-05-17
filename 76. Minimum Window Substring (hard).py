from collections import defaultdict


class SubstringWindow:
    def __init__(self, T_str):
        self.missing_letters_count = len(T_str)
        self.T_letters_dict = defaultdict(int)
        for letter in list(T_str):
            self.T_letters_dict[letter] += 1

        print("Intialized T_letters_dict to: ", str(self.T_letters_dict))

    def contains_all(self):
        return self.missing_letters_count == 0

    def in_T(self, letter):
        return letter in self.T_letters_dict

    # While parsing the string, we found a new letter.  Mark it as found
    def found_letter(self, letter):
        if letter in self.T_letters_dict:
            curr_count = self.T_letters_dict[letter] - 1
            self.T_letters_dict[letter] = curr_count
            if curr_count >= 0:
                self.missing_letters_count -= 1

    # While parsing the string, we have shortened the window and removed a
    # letter that was previously added as found.
    def unfound_letter(self, letter):
        if letter in self.T_letters_dict:
            curr_count = self.T_letters_dict[letter] + 1
            self.T_letters_dict[letter] = curr_count
            if curr_count > 0:
                self.missing_letters_count += 1

    @staticmethod
    def unit_test():
        to_find = "C"
        test_string = "ABCDCE"
        test_window = SubstringWindow(to_find)
        print("to_find = ", to_find)
        print("test_window.contains_all() returns ", str(test_window.contains_all()))
        print(f"marking found: the letters {test_string} to test_window")
        for l in test_string:
            test_window.found_letter(l)
            print(f"Added {l}, contains_all now returns {test_window.contains_all()}")

        print(f"unfinding the letters {test_string} in test_window")
        for l in "ACBC":
            test_window.unfound_letter(l)
            print(f"Removed {l}, contains_all now returns {test_window.contains_all()}")



def min_window_substr(s_string, t_string):
    window = SubstringWindow(t_string)
    w_start_idx, w_end_idx = 0, 0
    min_len_window, min_start, min_end = 0, 0, 0

    while w_end_idx < len(s_string):
        curr_letter = s_string[w_end_idx]
        window.found_letter(curr_letter)

        # While the current window contains all elements in t_string, shorten the window
        while window.contains_all():
            if (min_len_window) == 0 or (w_end_idx - w_end_idx <= min_len_window):
                min_start, min_end = w_start_idx, w_end_idx
                min_len_window = min_end - min_start + 1  # possible fencepost issue, check

            window.unfound_letter(s_string[w_start_idx])
            w_start_idx += 1

        w_end_idx += 1

    return (min_start, min_end)


def test_min_window(s_string, t_string):
    print("Test: calling min_window_substr(s_string, t_string):\n",
          f"s_string = \"{s_string}\"\n",
          f"t_string = \"{t_string}\"\n")
    min_start, min_end = min_window_substr(s_string, t_string)
    print(f"Returns ({min_start}, {min_end}), window={s_string[min_start:min_end+1]}")

#SubstringWindow.unit_test()
test_str = "ADOBECODEBANCBA"
test_t = "ABCC"
test_min_window(test_str, test_t)
