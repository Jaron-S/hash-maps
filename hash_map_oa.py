# Name: Jaron Schoorlemmer
# OSU Email: schoorja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: March 11th, 2022
# Description: A hash map implemented using open addressing with
#              quadratic probing.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Empties the table.
        """
        # iterate over the buckets and empty them
        for i in range(self.capacity):
            entry = self.buckets[i]
            self.buckets[i] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value of the given key.
        Returns None if the key does not exist.
        """
        # find the first corresponding bucket
        hash = self.hash_function(key) % self.capacity
        bucket = self.buckets[hash]
        # probe quadratically until a match or None type is found
        j = 1
        while bucket is not None:
            # if a match is found, return its value
            if bucket.key == key and bucket.is_tombstone == False:
                return bucket.value
            # otherwise, get the next bucket
            new_hash = (hash + j ** 2) % self.capacity
            bucket = self.buckets[new_hash]
            j += 1
        # if no matching key was found
        return None

    def put(self, key: str, value: object) -> None:
        """
        Adds a key/value pair to the table.
        """
        # the load factor is over 0.5, resize the table
        temp = self.table_load()
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)
        # find the entry at the corresponding hash index
        hash = self.hash_function(key) % self.capacity
        bucket = self.buckets[hash]
        # if the bucket is not empty, check for a key match
        # if not found, search for the next bucket quadratically
        j = 1
        new_hash = hash
        while bucket is not None:
            # if the key matches, replace the value and end the loop
            if bucket.key == key:
                bucket.value = value
                # if the entry was a tombstone, update size
                if bucket.is_tombstone:
                    self.size += 1
                break
            # otherwise, find the next bucket
            else:
                new_hash = (hash + (j ** 2)) % self.capacity
                bucket = self.buckets[new_hash]
                j += 1
        # if an empty slot was found (i.e. key wasn't in the table),
        # insert the new entry
        if bucket is None or bucket.is_tombstone:
            self.buckets[new_hash] = HashEntry(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the key/value pair with the given key.
        """
        # find the first corresponding bucket
        hash = self.hash_function(key) % self.capacity
        bucket = self.buckets[hash]
        # probe quadratically until a match or None type is found
        j = 1
        while bucket is not None:
            # if a match is found, remove it and stop probing
            if bucket.key == key and bucket.is_tombstone is False:
                bucket.is_tombstone = True
                self.size -= 1
                break
            # otherwise, get the next bucket
            new_hash = (hash + j ** 2) % self.capacity
            bucket = self.buckets[new_hash]
            j += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the table, False otherwise.
        """
        # find the first bucket that corresponds to that key
        hash = self.hash_function(key) % self.capacity
        bucket = self.buckets[hash]
        # probe quadratically for the key
        j = 1
        while bucket is not None:
            # if there is a match, return True
            if bucket.key == key and bucket.is_tombstone is False:
                return True
            # otherwise, check the next bucket
            new_hash = (hash + (j ** 2)) % self.capacity
            bucket = self.buckets[new_hash]
            j += 1
        # we reach a None object, the key is not in the table
        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Returns the load factor.
        (fractional ratio of filled vs. empty buckets)
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the size of the table to the new capacity.
        """
        # if the capacity is below 0 or the current size, stop and do nothing
        if new_capacity < 1 or new_capacity < self.size:
            return
        # create a new hash map
        new_map = HashMap(new_capacity, self.hash_function)
        # iterate over the entries and move them into the new table
        for i in range(self.capacity):
            bucket = self.buckets[i]
            # if there is an entry in this bucket,
            # place it in the new hash table
            if bucket and bucket.is_tombstone is False:
                new_map.put(bucket.key, bucket.value)
        # update the hash table
        self.buckets = new_map.buckets
        self.capacity = new_map.capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns an array of all the keys in the table.
        """
        # iterate over the table and collect the keys
        keys = DynamicArray()
        for i in range(self.capacity):
            bucket = self.buckets[i]
            if bucket is not None and bucket.is_tombstone is False:
                keys.append(bucket.key)

        return keys


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
