"""A magical string S consists of only '1' and '2' and obeys the following rules:

The string S is magical because concatenating the number of contiguous occurrences of characters '1' and '2' generates the string S itSolution.
The first few elements of string S is the following: S = "1221121221221121122……"
If we group the consecutive '1's and '2's in S, it will be:
    1 22 11 2 1 22 1 22 11 2 11 22 ......
and the occurrences of '1's or '2's in each group are:
    1 2	2 1 1 2 1 2 2 1 2 2 ......
You can see that the occurrence sequence above is the S itSolution.

Given an integer N as input, return the number of '1's in the first N number in the magical string S.
Note: N will not exceed 100,000.

Example 1:
Input: 6
Output: 3
Explanation: The first 6 elements of magical string S is "12211" and it contains three 1's, so return 3.
"""

class Solution:

    # Class global variables
    magic_string = [1, 2, 2]
    magic_string_len = 3
    pointer = 2
    last_num = 2
    ones = [1, 1, 1]

    def magicalString(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n <= Solution.magic_string_len:
            return Solution.ones[n-1]

        last_one = Solution.ones[-1]
        while n > Solution.magic_string_len:
            Solution.last_num = 3 - Solution.last_num
            times = Solution.magic_string[Solution.pointer]
            Solution.magic_string.append(Solution.last_num)
            if Solution.last_num == 1:
                last_one += 1

            Solution.ones.append(last_one)
            if times == 2:
                if Solution.last_num == 1:
                    last_one += 1
                Solution.ones.append(last_one)
                Solution.magic_string.append(Solution.last_num)

            Solution.pointer += 1
            Solution.magic_string_len += times

        # print("".join(map(str, Solution.magic_string)))
        # print("ms[0:n].count(1) returns ", Solution.magic_string.count(1))
        # print("ones is ", str(Solution.ones))
        # print("ones[n-1] returns ", Solution.ones[n-1])

        return Solution.ones[n-1]


Solution().magicalString(15)