class Solution:
    def isPalindrome(self, x: int) -> bool:
        x=str(x)
        rev=x[::-1]
        print(x)
        if x[0]=='-':
            return False
        return x==rev
        