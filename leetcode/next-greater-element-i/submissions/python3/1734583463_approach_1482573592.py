class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        dt={}
        st=[-1]*len(nums1)
        for i in range(len(nums2)-1):
            for j in range(i+1,len(nums2)):
                if nums2[j]>nums2[i]:
                    dt[nums2[i]]=nums2[j]
                    break
        print(dt)
        for i in range(len(nums1)):
            if nums1[i] in dt:
                st[i]=dt[nums1[i]]
        return st


        
            
                
        