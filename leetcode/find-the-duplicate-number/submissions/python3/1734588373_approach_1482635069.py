class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        dt={}
        for n in nums:
            if n in dt:
                return n
            else:
                dt[n]=1
        