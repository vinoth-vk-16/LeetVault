class Solution:
    def sortColors(self, nums: List[int]) -> None:
        for i in range(1,len(nums)):
            j=i-1
            key=nums[i]

            while j>=0 and nums[j]>key:
                nums[j+1]=nums[j]
                j-=1

            nums[j+1]=key
            
        