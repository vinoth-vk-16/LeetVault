class Solution:
    def climbStairs(self, n: int) -> int:
        if n==1:
            return 1
        if n==2:
            return n
        if n==3:
            return n
        a=2
        b=3
        for _ in range(4,n+1):
            a,b=b,a+b
        return b