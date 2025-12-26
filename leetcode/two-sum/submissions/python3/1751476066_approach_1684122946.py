class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dt={}
        for i in range(0,len(nums)):
            if target-nums[i] in dt:
                return i,dt[target-nums[i]]
            dt[nums[i]]=i
        
        