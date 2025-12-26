class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ps=0
        cnt=0
        dt={0:1}
        for i in range(len(nums)):
            ps+=nums[i]
            if ps-k in dt:
                cnt+=dt[ps-k]
            if ps in dt:
                dt[ps]+=1
            else:
                dt[ps]=1
        return cnt
            
        

        