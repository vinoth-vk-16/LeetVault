class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        max_length=0
        subs=""
        for char in s:
            if char not in subs:
                subs+=char
                max_length= max(max_length, len(subs))
            else:
                index =subs.index(char)
                subs = subs[index + 1:] + char     
 
        return max_length

        