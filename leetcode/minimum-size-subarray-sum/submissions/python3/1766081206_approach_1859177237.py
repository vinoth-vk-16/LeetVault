class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        res=float('inf')
        l,r,tot=0,0,0
        for r in range(len(nums)):
            tot+=nums[r]
            while tot>=target:
                res=min(res,r-l+1)
                tot-=nums[l]
                l+=1
        return 0 if res==float('inf') else res

       