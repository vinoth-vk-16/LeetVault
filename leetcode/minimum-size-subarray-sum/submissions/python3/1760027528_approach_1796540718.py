class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_len=float('inf')
        l=0
        r=0
        summ=nums[0]
        while r<=len(nums):
            if summ>=target:
                print(summ,"l")
                min_len=min(min_len,(r+1-l))
                summ-=nums[l]
                l+=1
                
            else:
                
                r+=1
                if r<len(nums):
                    summ+=nums[r]
                
        if min_len!=float('inf'):
            return min_len
        else:
            return 0
