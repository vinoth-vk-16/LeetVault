class Solution:
    def isValid(self, s: str) -> bool:
        stack=[]  #act as a stack
        closehas={')':'(','}':'{',']':'['}
        for ch in s:
            if ch in closehas:
                if stack and stack[-1]==closehas[ch]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(ch)
        if not stack:
            return True 
        else:
            False
             
        
        