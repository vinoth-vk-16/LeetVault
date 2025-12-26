class Solution:
    def findLHS(self, nums: List[int]) -> int:
        dt=Counter(nums)
        maxx=0
        m=0
        for val in dt:
            if val+1 in dt:
                m=dt[val]+dt[val+1]
                maxx=max(m,maxx)
        return maxx

        