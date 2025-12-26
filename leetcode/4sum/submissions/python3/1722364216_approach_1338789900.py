class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        quad=[]
        rem=[]
        def ksum(k,start,t):
            if k!=2:
                for i in range(start,len(nums)-k+1):
                    if i>start and nums[i]==nums[i-1]:
                        continue
                    quad.append(nums[i])
                    ksum(k-1,i+1,t-nums[i])
                    quad.pop()
                return
            #2sum
            l,r=start,len(nums)-1
            while l < r:
                if nums[l]+nums[r]< t:
                    l+=1
                elif nums[l]+nums[r]> t:
                    r-=1
                else:
                    rem.append(quad + [nums[l],nums[r]])
                    l+=1
                    while l<r and nums[l]==nums[l-1]:
                        l+=1

        ksum(4,0,target)
        return rem
        

        