class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        dt={}
        if len(s)!=len(t):
            return False
        for val in s:
            if val in dt:
                dt[val]+=1
            else:
                dt[val]=1
        for v in t:
            if v in dt and dt[v]>0:
                dt[v]-=1
            else:
                return False
        return True
            
        