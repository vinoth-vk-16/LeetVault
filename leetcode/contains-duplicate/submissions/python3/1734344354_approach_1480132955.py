class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        st=list(set(nums))
        return len(nums)!=len(st)
        