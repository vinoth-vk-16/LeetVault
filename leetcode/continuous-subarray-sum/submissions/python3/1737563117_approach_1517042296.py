class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        dt={0:-1}
        s=0
        for i in range(len(nums)):
            s+=nums[i]
            r=s%k
            if r not in dt:
                dt[r]=i
            else:
                if i-dt[r]>=2:
                    return True
        return False
            
        