class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        st1=0
        st2=0
        fin=""
        while st1<len(word1) and st2<len(word2):
            fin+=word1[st1]
            fin+=word2[st2]
            st1+=1
            st2+=1
        if st1<len(word1):
            fin+=word1[st1:]
        if st2<len(word2):
            fin+=word2[st2:]
        return fin
        