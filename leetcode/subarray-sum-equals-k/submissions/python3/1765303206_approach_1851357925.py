from collections import defaultdict
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        ps=0
        cnt=0
        seen=defaultdict(int)
        seen[0]=1
        for val in nums:
            ps+=val
            tar=ps-k
            if tar in seen:
                cnt+=seen[tar]
            seen[ps]+=1
        return cnt
            
        

        