class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        nums.sort()
        p=[]
        for i in range(0,len(nums),2):
            p.append([nums[i],nums[i+1]])
        res=0
        for val in p:
            a,b=val
            res+=a
        return res
        