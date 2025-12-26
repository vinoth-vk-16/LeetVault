class Solution:
    def romanToInt(self, s: str) -> int:
        dictt={
            "I":1,
            "V":5,
            "X":10,
            "L":50,
            "C":100,
            "D":500,
            "M":1000
        }
        inte=0
        for i in range(len(s)):
            if i<len(s)-1 and dictt[s[i]]<dictt[s[i+1]]:
                inte-=dictt[s[i]]
            else:
                inte+=dictt[s[i]]
        return inte
        