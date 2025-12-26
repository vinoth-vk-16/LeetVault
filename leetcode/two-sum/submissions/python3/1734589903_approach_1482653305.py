class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictt={}
        for i in range(len(nums)):
            if (target-nums[i]) in dictt:
                return [i,dictt[target-nums[i]]]
            else:
                dictt[nums[i]]=i

        