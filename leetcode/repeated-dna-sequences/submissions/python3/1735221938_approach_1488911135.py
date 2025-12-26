class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        seen=set()
        l=0
        r=9
        arr=set()
        while r<len(s):
            if s[l:l+10] in seen:
                arr.add(s[l:l+10])
            seen.add(s[l:l+10])
            l+=1
            r+=1
        return list(arr)

        