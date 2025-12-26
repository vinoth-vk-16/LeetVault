class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l,r=0,0
        al=float("inf")
        rs=0
        for r in range(len(nums)):
            rs+=nums[r]
            while rs>=target:
                al=min(r-l+1,al)
                rs-=nums[l]
                l+=1
        if al!=float("inf"):
            return al
        else:
            return 0