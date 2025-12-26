class Solution:
    def validPalindrome(self, s: str) -> bool:
        def ispal(i,j):
            while i<j:
                if s[i]!=s[j]:
                    return False             
                i+=1
                j-=1
            return True

        
        l,r=0,len(s)-1
        while l<r:
            if s[l]==s[r]:
                l+=1
                r-=1
            else:
                return ispal(l+1,r) or ispal(l,r-1)
        return True

        
        

        