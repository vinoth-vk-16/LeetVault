
class Solution:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        cnt=0
        prefix_cnt=defaultdict(int)
        prefix_cnt[0]=1
        prefix_sum=0
        for num in nums:
            prefix_sum+=num
            if prefix_sum-goal >=0:
                cnt+=prefix_cnt[prefix_sum-goal]
            prefix_cnt[prefix_sum]+=1
        return cnt

        