"""Given a positive integer, output its complement number. The complement strategy is to flip the bits of its binary representation.

Note:
The given integer is guaranteed to fit within the range of a 32-bit signed integer.
You could assume no leading zero bit in the integer’s binary representation.
Example 1:
Input: 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits)

Input: 1
Output: 0
Explanation: The binary representation of 1 is 1 (no leading zero bits), and its complement is 0. So you need to output 0.
"""

class Solution:
    def findComplement(self, num):
        """
        :type num: int
        :rtype: int
        """

        savenum = num
        result = None
        highest = 1
        while num:
            # print("num={}, highest={}".format(num, highest))
            highest *= 2  #Increment highest non-zero bit
            num = num // 2

        # print("num={}, highest={}".format(num, highest))

        # Create a number that has the same number of bits as num, but they are all 1
        highest -= 1
        #   print("highest is ", highest)
        result = highest - savenum
        #   print("returning result ", result)
        return result


    @staticmethod
    def findComplement_test():
        s = Solution()
        for input in [5, 1, 7, 15, 33, 32]:
            complement = s.findComplement(input)
            print("for input {:2d}, the output was {}".format(input, complement))


Solution.findComplement_test()