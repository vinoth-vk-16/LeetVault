class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        df={}
        for i in range(len(nums)):
            if target-nums[i] in df:
                return [i,df[target-nums[i]]]
            df[nums[i]]=i
        
        