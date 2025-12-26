class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        dt={}
        if len(s)!=len(t):
            return False
        s=list(s)
        t=list(t)
        s.sort()
        t.sort()
        i=0
        for val in s:
            if val==t[i]:
                i+=1
            else:
                return False
        return True