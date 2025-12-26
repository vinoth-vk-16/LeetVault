class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x:x[1])
        end=float("-inf")
        cnt=0
        for st,finish in intervals:
            if st>=end:
                end=finish
            else:
                cnt+=1
        return cnt

        

        