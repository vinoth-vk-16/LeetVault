class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        dt={0:1}
        cnt=0
        s=0
        for i,val in enumerate(nums):
            s+=nums[i]
            v=s-k
            if v in dt:
                cnt+=dt[v]
            if s in dt:
                dt[s]+=1
            else:
                dt[s]=1
        return cnt


        
        