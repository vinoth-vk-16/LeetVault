class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        dt={}
        for n in nums:
            dt[n]=dt.get(n,0)+1
        for x in dt:
            if dt[x]>1:
                return x
        