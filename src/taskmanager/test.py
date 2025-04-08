def merge(self,other):
    #check if empty
    if other.head.next == other.head:
        return

    last_value_l1 = self.head.prev
    first_value_l2 = other.head.next
    last_value_l2 = other.head.prev

    last_value_l1.next =  first_value_l2
    first_value_l2.prev = last_value_l1
    last_value_l2.next  = self.head
    self.head.prev = last_value_l2

def delete_all(self,val):
    current = self.top
    previous = None

    while current:
        if current.val == val:
            if previous:
                previous.next = current.next
            else:
                self.top = current.next
        else:
            previous = current

        current = current.next




