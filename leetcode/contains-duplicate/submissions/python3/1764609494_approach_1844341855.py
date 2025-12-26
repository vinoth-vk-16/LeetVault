class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        n=len(nums)
        n1=len(set(nums))
        return n!=n1

        