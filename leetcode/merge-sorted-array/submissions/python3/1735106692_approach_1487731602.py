class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        a=m-1
        b=m+n-1
        c=n-1
        while c>=0:
            if a>=0 and nums1[a]>nums2[c]:
                nums1[b]=nums1[a]
                a-=1
            else:
                nums1[b]=nums2[c]
                c-=1
            b-=1

       
        
        