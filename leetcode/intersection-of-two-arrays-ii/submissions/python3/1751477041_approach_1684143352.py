class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        fin=[]
        for num in nums1:
            if num in nums2:
                fin.append(num)
                nums2.remove(num)
        return fin

        