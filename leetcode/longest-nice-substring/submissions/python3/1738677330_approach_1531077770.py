class Solution:
    def longestNiceSubstring(self, s: str) -> str:
        nc=""
        for i in range(len(s)):
            for j in range(1,len(s)):
                idd=True
                for val in s[i:j+1]:
                    if val.islower() and val.upper() not in s[i:j+1]:
                        idd=False
                    if val.isupper() and val.lower() not in s[i:j+1]:
                        idd=False
                if idd and len(s[i:j+1])>len(nc):
                    nc=s[i:j+1]
        return nc



        