class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        fin = []
        n = len(nums)
        nums.sort()
        
        if nums[0] != 1:
            fin.extend(range(1, nums[0]))
        
        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                continue
            if nums[i + 1] != nums[i] + 1:
                fin.extend(range(nums[i] + 1, nums[i + 1]))
        
        if nums[-1] != n:
            fin.extend(range(nums[-1] + 1, n + 1))
        
        return fin

        