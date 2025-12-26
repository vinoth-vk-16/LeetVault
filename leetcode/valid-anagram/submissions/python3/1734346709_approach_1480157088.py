class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        
        v1=''.join(sorted(s))
        v2=''.join(sorted(t))
        return v1==v2
        