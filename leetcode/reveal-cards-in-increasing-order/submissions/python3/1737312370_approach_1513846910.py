class Solution:
    def deckRevealedIncreasing(self, deck: List[int]) -> List[int]:
        nl=deque()
        deck.sort()
        for _ in range(len(deck)):
            if len(nl)==0:
                a=deck.pop()
                nl.append(a)
            else:
                a=nl.popleft()
                nl.append(a)
                nl.append(deck.pop())
        nl.reverse()
        return list(nl)
        
            


            

            
        