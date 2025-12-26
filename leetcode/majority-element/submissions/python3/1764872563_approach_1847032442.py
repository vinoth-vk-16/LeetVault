class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        df={}
        for val in nums:
            if val in df:
                df[val]+=1
            else:
                df[val]=1
        print(df)
        return (max(df,key=df.get))

        