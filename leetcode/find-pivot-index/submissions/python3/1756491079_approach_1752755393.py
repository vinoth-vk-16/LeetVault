class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        a=sum(nums)
        sn=0
        for i in range(len(nums)):
            if sn==(a-sn-nums[i]):
                return i
            sn+=nums[i]
        return -1
        