class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        uni=set()
        maxi=0
        l=0
        for r in range(len(s)):
            while s[r] in uni:
                uni.remove(s[l])
                l+=1
            uni.add(s[r])
            maxi=max(maxi,r-l+1)
        return maxi
