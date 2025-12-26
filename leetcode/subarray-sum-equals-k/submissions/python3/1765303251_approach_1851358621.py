class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ps=0
        cnt=0
        seen={0:1}
        seen[0]=1
        for val in nums:
            ps+=val
            tar=ps-k
            if tar in seen:
                cnt+=seen[tar]
            seen[ps]=seen.get(ps,0)+1
        return cnt
            
        

        