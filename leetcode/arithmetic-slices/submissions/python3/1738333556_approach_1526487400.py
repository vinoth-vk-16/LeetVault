class Solution:
    def numberOfArithmeticSlices(self, nums: List[int]) -> int:
        l=0
        r=2
        cnt=0
        fin=0
        for i in range(2,len(nums)):
            if nums[i]-nums[i-1]==nums[i-1]-nums[i-2]:
                cnt+=1
                fin+=cnt
            else:
                cnt=0
        return fin


        