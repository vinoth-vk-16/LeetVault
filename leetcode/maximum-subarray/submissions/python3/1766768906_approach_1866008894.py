class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        ms=nums[0]
        cs=nums[0]
        for i in range(1,len(nums)):
            cs=max(nums[i],cs+nums[i])
            if cs>ms:
                ms=cs
        return ms


        