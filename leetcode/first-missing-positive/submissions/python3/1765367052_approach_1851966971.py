class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        i=0
        n=len(nums)
        while i<n:
            x=nums[i]
            crct=x-1
            if 1<=x<=n and nums[crct]!=x:
                nums[i],nums[crct]=nums[crct],nums[i]
            else:
                i+=1

        for j in range(n):
            if nums[j]!=j+1:
                return j+1
        return n+1

        
        
            
        