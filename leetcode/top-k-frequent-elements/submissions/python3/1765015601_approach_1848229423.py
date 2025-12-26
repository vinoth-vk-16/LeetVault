class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        dt=Counter(nums)
        return (sorted(dt,key=dt.get, reverse= True)[:k])

        