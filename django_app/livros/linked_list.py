import threading


class Node:
    def __init__(self, data: dict):
        self.data = data
        self.next: "Node | None" = None


class LinkedList:
    def __init__(self):
        self.head: Node | None = None
        self.size: int = 0
        self._counter: int = 0
        self._lock = threading.Lock()

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def append(self, data: dict) -> dict:
        with self._lock:
            data["id"] = self._next_id()
            node = Node(data)
            if self.head is None:
                self.head = node
            else:
                current = self.head
                while current.next is not None:
                    current = current.next
                current.next = node
            self.size += 1
        return data

    def to_list(self) -> list[dict]:
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def find_by_id(self, book_id: int) -> dict | None:
        current = self.head
        while current is not None:
            if current.data["id"] == book_id:
                return current.data
            current = current.next
        return None

    def remove(self, book_id: int) -> bool:
        with self._lock:
            if self.head is None:
                return False

            if self.head.data["id"] == book_id:
                self.head = self.head.next
                self.size -= 1
                return True

            current = self.head
            while current.next is not None:
                if current.next.data["id"] == book_id:
                    current.next = current.next.next
                    self.size -= 1
                    return True
                current = current.next

        return False

    def update(self, book_id: int, new_data: dict) -> dict | None:
        with self._lock:
            current = self.head
            while current is not None:
                if current.data["id"] == book_id:
                    new_data["id"] = book_id
                    current.data = new_data
                    return current.data
                current = current.next
        return None


livros_db = LinkedList()