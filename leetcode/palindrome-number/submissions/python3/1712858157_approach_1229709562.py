class Solution:
    def isPalindrome(self, x: int) -> bool:
        result=0
        s1=str(x)
        if s1[0]=="-":
            return False
        for val in reversed(s1):
            result=result*10+int(val)
        if result==x:
            return True
        else:
            return False

        