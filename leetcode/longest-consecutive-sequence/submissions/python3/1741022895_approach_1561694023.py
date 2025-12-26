class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums=set(nums)
        nums=list(nums)
        nums.sort()
        print(nums)
        l,r=0,1
        m=1
        ma=1
        while r<len(nums):
            if nums[r]==nums[l]+1 :       
                m+=1
                l+=1
                ma=max(m,ma)
            else:
                l=r
                m=1
            r+=1
        return ma



