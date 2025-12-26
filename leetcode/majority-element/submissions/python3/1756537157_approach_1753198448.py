class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        dt={}
        for val in nums:
            if val in dt:
                dt[val]+=1
            else:
                dt[val]=1
        print(dt)
        return max(dt,key=dt.get)

        