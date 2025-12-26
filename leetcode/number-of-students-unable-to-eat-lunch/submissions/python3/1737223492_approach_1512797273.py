class Solution:
    def countStudents(self, students: List[int], sandwiches: List[int]) -> int:
        students=deque(students)
        sandwiches=deque(sandwiches)
        cnt=0
        l=len(students)*10
        while students:
            cnt+=1
            if sandwiches[0]==students[0]:
                sandwiches.popleft()
                students.popleft()
            else:
                a=students.popleft()
                students.append(a)
            if sandwiches and sandwiches[0] not in students:
                break
        return len(students)
            
            


        
        