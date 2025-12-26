class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        max_prd=nums[0]
        min_prod=nums[0]
        max_prod=nums[0]
        nums=nums[1:]
        for val in nums:
            if val<0:
                min_prod,max_prod=max_prod,min_prod
            min_prod=min(val,val*min_prod)
            max_prod=max(val,val*max_prod)
            max_prd=max(max_prd,max_prod)
        return max_prd




        

        