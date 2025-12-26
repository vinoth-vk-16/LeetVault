class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictt={}
        for i in range(len(nums)):
            val=(target-nums[i])
            if val in dictt:
                return [i,dictt[val]]
            else:
                dictt[nums[i]]=i

        