class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        db=(s+s)[1:-1]
        return s in db
        


        