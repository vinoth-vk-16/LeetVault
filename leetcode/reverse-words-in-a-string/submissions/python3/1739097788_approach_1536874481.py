class Solution:
    def reverseWords(self, s: str) -> str:
        s=s.split(" ")
        print(s)
        ns=""
        for val in reversed(s):
            if val.isalnum():
                ns+=val
                ns+=" "
        ns=ns[:-1]
        return ns

        