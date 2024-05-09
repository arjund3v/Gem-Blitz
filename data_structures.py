class Stack:

    def __init__(self, cap=10):
        self.stack = [None] * cap
        self.cap = cap
        self.size = 0

    def capacity(self):
        return self.cap

    def push(self, data):
		# If the size is the capacity, we resize
        if self.size == self.cap:
			# Initialize a new stack with double the capacity
            newStack = [None] * (self.cap*2)
			# Copy over the elements from the current stack to the new one
            for i in range(self.__len__()):
                newStack[i] = self.stack[i]
			# Point the current stack to the new stack
            self.stack = newStack
			# Set the new capacity
            self.cap = self.cap * 2

		# Whether we resize or not, this piece of code is always ran to add an item to the stack
        self.stack[self.size] = data
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError('pop() used on empty stack')

		# We get the removed item before removing it
        removedItem = self.stack[self.size - 1]
		# Pop off the most recent item
        self.stack[self.size - 1] = None
        self.size -= 1

        return removedItem

    def get_top(self):
        if self.is_empty():
            return None
        else:
            return self.stack[self.size - 1]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size


class Queue:
    def __init__(self, cap=10):
        # Initializes the Queue with a given capacity or a default of 10 if not provided.
        # The _queue will store our elements, and _front and _size will help manage them.
        self._queue = [None] * cap
        self._front = 0  # Index of the front element
        self._size = 0  # Number of elements currently in the queue
        self._capacity = cap

    def capacity(self):
        # Returns the capacity of the Queue.
        return self._capacity

    def enqueue(self, data):
        # If the queue is full, resize it (double the capacity)
        if self._size == self._capacity:
            self._resize(2 * self._capacity)

        # Adds data to the back of the Queue.
        back_index = (self._front + self._size) % self._capacity
        self._queue[back_index] = data
        self._size += 1

    def dequeue(self):
        # If the queue is empty, raise an error.
        if self.is_empty():
            raise IndexError('dequeue() used on empty queue')

        # Removes the oldest value from the Queue and returns it.
        data = self._queue[self._front]
        self._queue[self._front] = None  # Optional: free up space
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return data

    def get_front(self):
        # Returns the oldest value from the Queue without removing it.
        # Returns None if the Queue is empty.
        if self.is_empty():
            return None
        return self._queue[self._front]

    def is_empty(self):
        # Returns True if the Queue is empty, False otherwise.
        return self._size == 0

    def __len__(self):
        # Returns the number of values in the Queue.
        return self._size

    def _resize(self, new_capacity):
        # Private method to resize the underlying list.
        new_queue = [None] * new_capacity
        for i in range(self._size):
            new_queue[i] = self._queue[(self._front + i) % self._capacity]
        self._queue = new_queue
        self._front = 0
        self._capacity = new_capacity

class Deque:
    def __init__(self, cap=10):
        self.deque = [None] * cap
        self.cap = cap
        self.size = 0
        self.front = 0
        self.back = 0

    def capacity(self):
        return self.cap

    def push_front(self, data):
        self._resize()
        self.front = (self.front - 1) % self.cap
        self.deque[self.front] = data
        self.size += 1

    def push_back(self, data):
        self._resize()
        self.deque[self.back] = data
        self.back = (self.back + 1) % self.cap
        self.size += 1

    def pop_front(self):
        if self.size == 0:
            raise IndexError('pop_front() used on empty deque')
        popped_item = self.deque[self.front]
        self.front = (self.front + 1) % self.cap
        self.size -= 1
        return popped_item

    def pop_back(self):
        if self.size == 0:
            raise IndexError('pop_back() used on empty deque')
        self.back = (self.back - 1) % self.cap
        popped_item = self.deque[self.back]
        self.size -= 1
        return popped_item

    def _resize(self):
        if self.size == self.cap:
            self.cap *= 2
            new_deque = [None] * self.cap
            for i in range(self.size):
                new_deque[i] = self.deque[(self.front + i) % (self.cap // 2)]
            self.deque = new_deque
            self.front = 0
            self.back = self.size

    def get_front(self):
        if self.size == 0:
            return None
        return self.deque[self.front]

    def get_back(self):
        if self.size == 0:
            return None
        return self.deque[(self.back - 1) % self.cap]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def __getitem__(self, k):
        if k < 0 or k >= self.size:
            raise IndexError('Index out of range')
        return self.deque[(self.front + k) % self.cap]
