class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        a=len(nums)
        a1=len(set(nums))
        return a!=a1

        