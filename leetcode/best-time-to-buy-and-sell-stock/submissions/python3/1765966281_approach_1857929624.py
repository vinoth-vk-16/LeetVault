class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l,r=0,0
        maxi=0
        for r in range(1,len(prices)):
            if prices[l]<prices[r]:
                maxi=max(maxi,prices[r]-prices[l])
            else:
                l=r
        return maxi
        


        