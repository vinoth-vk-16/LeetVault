class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dt={}
        for i in range(len(nums)):
            if target-nums[i] in dt:
                return [dt[target-nums[i]],i]
            dt[nums[i]]=i