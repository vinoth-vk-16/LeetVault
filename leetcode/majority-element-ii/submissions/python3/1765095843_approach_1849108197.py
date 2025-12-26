class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        arr=Counter(nums)
        k=(len(nums)//3)
        fin=[]
        for val in arr:
            if arr[val]>k:
                fin.append(val)

        return fin
