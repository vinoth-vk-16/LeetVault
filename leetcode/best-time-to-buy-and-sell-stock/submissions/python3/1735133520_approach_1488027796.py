class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_val=float('inf')
        res=0
        for price in prices:
            if price<min_val:
                min_val=price
            else:
                res=max(res,price-min_val)
        return res    
        
            