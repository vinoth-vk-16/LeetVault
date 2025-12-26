class Solution:
    def findLHS(self, nums: List[int]) -> int:
        nums.sort()
        l,r=0,0
        m=0
        maxx=0
        while r<len(nums):
            if nums[r]-nums[l]==1:
                m=(r-l+1)
                maxx=max(m,maxx)
                r+=1
            elif nums[r]-nums[l]>1:
                l+=1
                m=0
            elif nums[r]==nums[l]:
                r+=1
        return maxx



        