class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        ms=sum(nums[:k])
        curr=ms
        r=k
        l=0
        while r<len(nums):
            curr-=nums[l]
            curr+=nums[r]
            ms=max(ms,curr)
            l+=1
            r+=1
        return ms/k
            


        