class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l=0
        sm=float("inf")
        cs=0
        for r in range(len(nums)):
            cs+=nums[r]
            while cs>=target:
                sm=min(sm,r-l+1)
                cs-=nums[l]
                l+=1
        if sm!=float("inf"):
            return sm
        else:
            return 0
                    

       