class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort()
        n=len(citations)
        for val in citations:
            if val>=n:
                return n
            n-=1
        return 0

        