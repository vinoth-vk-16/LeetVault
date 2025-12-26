class Solution:
    def isPalindrome(self, s: str) -> bool:
        al=""
        for val in s:
            if val.isalnum():
                al+=val
        
        al=al.lower()
        la=al[::-1]
        return al==la
