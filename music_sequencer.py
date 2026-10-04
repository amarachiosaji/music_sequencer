from doubly_linked_list import LinkedList
from midi_player import MidiPlayer


class MusicSequencer:
    def __init__(self):
        self._composition: LinkedList = LinkedList()
        self._current_index: int = -1  # -1 == "no current" (empty composition)
        self._player = MidiPlayer()

   
    def size(self) -> int:
        return self._composition.size()

    def is_empty(self) -> bool:
        return self._composition.is_empty()

    def current_index(self) -> int:
        return self._current_index

    def current_phrase(self) -> str:
        if self._current_index == -1:
            raise IndexError("current_phrase: composition is empty, there is no current phrase")
        return self._composition.get(self._current_index)

    def __str__(self) -> str:
        return str(self._composition)

    def __iter__(self):
        """Delegate iteration to the underlying list (yields phrase strings only)."""
        return iter(self._composition)

    
    def insert_front(self, phrase: str) -> None:
        was_empty = self.is_empty()
        self._composition.insert_first(phrase)
        if was_empty:
            self._current_index = 0
        else:
            self._current_index += 1  # everything that existed shifted right by one

    def insert_back(self, phrase: str) -> None:
        was_empty = self.is_empty()
        self._composition.insert_last(phrase)
        if was_empty:
            self._current_index = 0
        
    def insert_current(self, phrase: str) -> None:
        """Insert immediately after the current position."""
        if self.is_empty():
            self.insert_back(phrase)
            return
        self._composition.insert_at(self._current_index + 1, phrase)
        
    def repeat_current(self) -> None:
        """Duplicate the phrase at current, append the duplicate to the end."""
        phrase = self.current_phrase()  # raises IndexError if empty
        self._composition.insert_last(phrase)

    
    def remove_current(self) -> str:
        if self.is_empty():
            raise IndexError("remove_current: composition is empty")

        removed = self._composition.remove_at(self._current_index)

        if self.is_empty():
            self._current_index = -1
        elif self._current_index >= self.size():
            self._current_index = self.size() - 1
        
        return removed

    def remove_specific(self, index: int) -> str:
        if index < 0 or index >= self.size():
            raise IndexError(f"remove_specific: index {index} out of bounds for size {self.size()}")

        removed = self._composition.remove_at(index)

        if self.is_empty():
            self._current_index = -1
        elif index < self._current_index:
            self._current_index -= 1  # current's logical phrase shifted left by one
        elif index == self._current_index and self._current_index >= self.size():
            self._current_index = self.size() - 1  # removed current AND it was the tail

        return removed

    
    def move_phrase(self, source_index: int, target_index: int, *, verbose: bool = False) -> None:
        self._composition.move(source_index, target_index, verbose=verbose)

        if self._current_index == source_index:
            self._current_index = target_index
        elif source_index < self._current_index <= target_index:
            self._current_index -= 1
        elif target_index <= self._current_index < source_index:
            self._current_index += 1

    
    def play_all(self) -> None:
        for phrase in self._composition:
            self._player.play(phrase)

    def play_from_current(self) -> None:
        if self.is_empty():
            return
        for phrase in self._composition.iter_from(self._current_index):
            self._player.play(phrase)

    def play_current(self) -> None:
        self._player.play(self.current_phrase())

    
    def move_forward(self) -> None:
        if self._current_index < self.size() - 1:
            self._current_index += 1
        
    def move_backward(self) -> None:
        if self._current_index > 0:
            self._current_index -= 1
        
    
    def close(self) -> None:
        self._player.close()