class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        l,r=0,0
        fin=""
        while l<len(word1) or r<len(word2):
            if l<len(word1):
                fin+=(word1[l])
                l+=1
            if r<len(word2):
                fin+=(word2[r])
                r+=1
        return fin
        