class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        nums=sorted(set(nums))
        n=1
        for i in range(len(nums)):
            if nums[i]<1:
                continue
            if nums[i]!=n:
                return n
            n+=1
        return n


        
        
            
        