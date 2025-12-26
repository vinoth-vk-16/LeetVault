class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        dt={}
        for val in magazine:
            if val not in dt:
                dt[val]=1
            else:
                dt[val]+=1
        for val in ransomNote:
            if val not in dt or dt[val]==0:
                return False
            dt[val]-=1
        return True

        