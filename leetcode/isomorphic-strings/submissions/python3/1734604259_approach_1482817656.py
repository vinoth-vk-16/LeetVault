class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        r=set(zip(s,t))
        return len(set(s))==len(set(t))==len(r)
            


        