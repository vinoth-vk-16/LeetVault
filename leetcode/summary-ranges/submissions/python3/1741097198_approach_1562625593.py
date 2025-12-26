class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        arr=[] 
        l,r=0,0
        while r<len(nums):
            while r!=len(nums)-1 and nums[r]+1==nums[r+1]:
                r+=1
            st=str(nums[l])+"->"+str(nums[r])
            if nums[l]!=nums[r]:
                arr.append(st)
            else:
                arr.append(str(nums[l]))
            print(arr)
            r+=1
            l=r
        return arr
        