class MyHashMap:

    def __init__(self):
        self.arr=dict()

    def put(self, key: int, value: int) -> None:
        self.arr[key]=value
        
        
    def get(self, key: int) -> int:
        if key in self.arr:
            return self.arr[key]
        return -1
        

    def remove(self, key: int) -> None:
        if key in self.arr:
            del self.arr[key]

  


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)