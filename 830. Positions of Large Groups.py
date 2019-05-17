'''
In a string S of lowercase letters, these letters form consecutive groups of the same character.
For example, a string like S = "abbxxxxzyy" has the groups "a", "bb", "xxxx", "z" and "yy".
Call a group large if it has 3 or more characters.  We would like the starting and ending positions of every large group.
The final answer should be in lexicographic order.
1 <= S.length <= 1000
'''

class Solution:
    def largeGroupPositions(self, S):
        """
        :type S: str
        :rtype: List[List[int]]
        """

        lastchar = S[0]
        runstart = 0
        result = []
        for i, c in enumerate(S[1:]+"_", 1):
            if lastchar != c:
                if i - runstart > 2:
                    result.append([runstart, i-1])
                runstart = i
            lastchar = c


        return result

    @staticmethod
    def test():
        teststrings = [
            "abbxxxxzzy",
            "abc",
            "abcdddeeeeaabbbcd",
            "aaa"
        ]
        s = Solution()

        for ts in teststrings:
            result = s.largeGroupPositions(ts)
            print(f"largeGroupPositions(ts) yields: {result}")


Solution.test()
