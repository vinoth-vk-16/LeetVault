class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        pf=[0]*(len(nums))
        pf[0]=nums[0]
        sf=[0]*(len(nums))
        for i in range(1,len(nums)):
            pf[i]=pf[i-1]*nums[i]
        for j in range(len(nums)-1,-1,-1):
            if j == len(nums) - 1:  
                sf[j] = nums[j]
            else:
                sf[j] = sf[j + 1]* nums[j]
        res=[]
        for k in range(len(nums)):
            if k==0:
                res.append(sf[k+1])
            elif k==(len(nums)-1):
                res.append(pf[k-1])
            else:
                res.append(pf[k-1]*sf[k+1])
        return res



        

        