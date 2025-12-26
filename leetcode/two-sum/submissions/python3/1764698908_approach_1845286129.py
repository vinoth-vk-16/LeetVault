class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        df={}
        for val in range(0,len(nums)):
            if target-nums[val] in df:
                return [val,df[target-nums[val]]]
            else:
                df[nums[val]]=val
        
        