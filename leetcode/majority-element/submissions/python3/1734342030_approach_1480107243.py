class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        l1=list(set(nums))
        majo=0
        for l in l1:
            cnt=0
            for i in range(len(nums)):
                if (l==nums[i]):
                    cnt+=1
                    if cnt>majo:
                        majo=cnt
                        val=nums[i]
        return val
        
        