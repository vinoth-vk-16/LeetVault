class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l=0
        r=0
        cs=0
        lenn=float('inf')
        arr=[]
        while r<len(nums):
            cs+=nums[r]
            while cs>=target:

                if len(nums[l:r+1])<lenn:
                    lenn=len(nums[l:r+1])
                    arr=(nums[l:r+1])
                cs-=nums[l]
                l+=1
            r+=1
        return len(arr)
        
