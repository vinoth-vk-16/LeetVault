class Solution:
    def firstUniqChar(self, s: str) -> int:
        dictt=Counter(s)
        for val in dictt:
            if dictt[val]==1:
                return s.index(val)
        return -1
        