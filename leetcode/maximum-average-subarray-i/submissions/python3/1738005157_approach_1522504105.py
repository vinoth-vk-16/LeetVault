class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        r=k-1
        l=0
        max_av=float('-inf')
        av=0
        for i in range(1,len(nums)):
            nums[i]=nums[i-1]+nums[i]
        print(nums)
        while r<len(nums):
            if l==0:
                av=nums[r]/k
            else:
                av=(nums[r]-nums[l-1])/k
            l+=1
            r+=1
            max_av=max(av,max_av)
        return max_av
            


        