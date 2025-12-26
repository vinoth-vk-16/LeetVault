class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return 0 
        pf=[0]*len(nums)
        sf=[0]*len(nums)
        pf[0]=nums[0]
        sf[-1]=nums[-1]
        for i in range(1,len(nums)):
            pf[i]=pf[i-1]+nums[i]
        for i in range(len(nums)-2,-1,-1):
            sf[i]=sf[i+1]+nums[i]
        for j in range(len(nums)):
            if j==0:
                if j<len(nums)-1 and sf[j+1]==0:
                    return j
            elif j==len(nums)-1:
                if pf[j-1]==0:
                    return j
            else:
                if pf[j-1]==sf[j+1]:
                    return j
        return -1
        