class Solution:
    def firstUniqChar(self, s: str) -> int:
        new=''
        dictt=Counter(s)
        for val in dictt:
            if dictt[val]==1:
                new=val
                break
        
        if new:
            return s.index(new)
        else:
            return -1
        