from collections import Counter
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        cnt=0
        vote=nums[0]
        for n in nums:
            if cnt==0:
                vote=n
            if n==vote:
                cnt+=1
            else:
                if n!=vote:
                    cnt-=1
            
        return vote

        