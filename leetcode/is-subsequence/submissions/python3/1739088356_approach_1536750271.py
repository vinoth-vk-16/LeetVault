class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        l=0
        l1=0
        if s==t:
            return True
        for l1 in range(len(t)):
 
            if l<len(s) and t[l1]==s[l]:
                l+=1
            if l>=len(s):
                return True
        return False






        