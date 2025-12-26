class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums=set(nums)
        m=-999
        for val in nums:
            if val-1 not in nums:
                lenn=1
                while val+lenn in nums:
                    lenn+=1
                m=max(m,lenn)
        return m
                

