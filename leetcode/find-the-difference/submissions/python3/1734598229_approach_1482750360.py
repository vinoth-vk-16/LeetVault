class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        dt=Counter(s)
        dt1=Counter(t)
        for val in dt1:
            if dt1[val]!=dt.get(val,0):
                return val


        