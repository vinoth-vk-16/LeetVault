class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        hash1={0:1}
        summ=0
        no=0
        for i in range(0,len(nums)):
            summ+=nums[i]
            diff=summ-k
            if diff in hash1:
                no+=(hash1[diff])
            if summ not in hash1:
                hash1[summ]=1
            else:
                hash1[summ]+=1
        return no

        
          
            