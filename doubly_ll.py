from abc import ABC, abstractmethodfrom typing import TypeVar, Generic, Optional

T = TypeVar('T')

class _Node(Generic[T]):
    __slots__ = ('data', 'prev', 'next')

    def __init__(self, data: T):
        self.data: T = data
        self.prev: Optional['_Node[T]'] = None
        self.next: Optional['_Node[T]'] = None

class DoublyLL(ABC, Generic[T]):
    @abstractmethod
    def insert_first(self, element: T) -> None: pass

    @abstractmethod
    def insert_last(self, element: T) -> None: pass

    @abstractmethod
    def insert_at(self, index: int, element: T) -> None: pass

    @abstractmethod
    def remove_at(self, index: int) -> T: pass

    @abstractmethod
    def get(self, index: int) -> T: pass

    @abstractmethod
    def size(self) -> int: pass

    @abstractmethod
    def is_empty(self) -> bool: pass


class LList(DoublyLL[T]):

    def __init__(self):
        self._head: Optional[_Node[T]] = None
        self._tail: Optional[_Node[T]] = None
        self._size: int = 0


    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def insert_first(self, element: T) -> None:
        new_node = _Node(element)
        if self.is_empty():
            self._head = se;f._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def insert_last(self, element: T) -> None
        new_node = _Node(element)
        if self.is_empty():
            self._head = self._tail = new_node
        else: 
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

        def insert_at(self, index: int, element: T) -> None:
            if index < 0 or index > self._size:
                raise IndexError(f"insert_at: index {index} out of bounds for size {self._size}")
if index == 0:
    self.insert_first(element)
    return
if index == self._size:
    self.insert_last(element)
    return


successor = self._node_at(index)
predecessor = successor.prev

new_node = _Node(element)
new_node.prev = predecessor
new_node.next = successor
predecessor.next = new_node
successor.prev = new_node
self._size += 1


def remove_at(self, index: int) -> T:
    node = self._node_at(index)

    self._unlink(node)
    return node.data


def get(self, index: int) -> T:
    return self._node_at(index).data


def _node_at(self, index: int) -> _Node[T]:
    if index < 0 or index >= self._size
        raise IndexError(f"index {index} out of bounds for size {self._size}")

    if index <= self._size
        current = self._head
        for _ in range(index):
            current = current.next

    else:
        current = self._tail
        for _ in range(self._size - 1 - index):
            current = current.prev
    return current


def _unlink(self, node: _Node[T]) -> None:
    if node.prev is not None:
        node.prev.next = node.next
    else:
        self._head = node.next

    if node.next is not None:
        node.next.prev = node.prev
    else:
        self._tail = node.prev

    node.prev = None
    node.next = None
    self._size -= 1


def _link_at(self, node: _Node[T], index: int) -> None:
    if index < 0 or index > self._size:
        raise IndexError(f"index {index} out of bounds for size {self._size}")

    if self.is_empty():
        node.prev = node.next = None
        self._head = self._tail = node
    elif index == 0:
        node.prev = None
        node.next = self._head
        self._head.prev = node
        self._head = node
    elif index == self._size:
        node.next = None
        node.prev = self._tail
        self._tail.next = node
        self._tail = node
    else: 
        succesor = self._node_at(index)
        predecessor = successor.prev
        node.prev = predecessor
        node.next = successor
        predecessor.next = node
        successor.prev = node

    self._size += 1


    def move(self, source_index: int, target_index: int, *, verbose: bool = False) -> None:

        if source_index < 0 or source_index >= self._size:
            raise IndexError(f"move: target index {target_index} out of bounds")

        if target_index < 0 or target_index >= self._size:
            raise IndexError(f"move: target index {target_index} out of bounds")

        if source_index == target_index:
            return

        node = self._node_at(source_index)


        if verbose:
            print(f"Unlinking Node at Index {source_index} ({node.data}) ...", end="")
            self._unlink(node)

        if verbose:
            print("Successful.")

        if verbose:
            print(f"Re-linking Node at Index {target_index}...", end="")
            self._link_at(node, target_index)
        
        if verbose:
            print("Successful.")

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def iter_from(self, index: int):
        if index < 0 or index > self._size:
            raise IndexError(f"iter_from: index {index} out of bounds for size {self._size}")

        if index == self._size:
            return
        
        current = self._node_at(index)
        while current is not None:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        if self.is_empty():
            return "[ EMPTY ]"
        parts = ""
        current = self._head
        while current is not None:
            parts += f"[ {current.data} ]"
            if current.next is not None:
                parts += " <-> "
            current = current.next
        return parts
        
    
