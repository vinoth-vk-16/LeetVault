class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        l,r=0,len(people)-1
        fin=[]
        while l<r:
            if people[l]+people[r]<=limit:
                fin.append([people[l],people[r]])
                l+=1
                r-=1
            else:
                if people[l]>people[r]:
                    fin.append([l])
                    l+=1
                else:
                    fin.append([r])
                    r-=1
        if l==r:
            fin.append(people[r])
        return len(fin)



        