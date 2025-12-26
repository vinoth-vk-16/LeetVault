class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        n=set(nums)
        n=list(n)
        n.sort()
        print(n)
        if len(n)<3:
            return n[-1]
        else:
            return n[-3]
        