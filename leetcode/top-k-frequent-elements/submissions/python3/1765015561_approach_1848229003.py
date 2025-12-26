class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        nums1=list(set(nums))
        dt={}
        for val in nums1:
            dt[val]=nums.count(val)
        return (sorted(dt,key=dt.get, reverse= True)[:k])

        