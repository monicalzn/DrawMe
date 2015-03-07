import sys
class HashTable():
	def __init__(self):
		self._table = [None] * 3
		self._numEntries = 0

	def put(self, key, value):
		"""Inserts a value by a key into the hash table."""
		if (self._numEntries > len(self._table)/2):
			self._grow()
		hc = self._hashcode(key)
		i = hc % len(self._table)
		# TODO: make a pluggable 'probe' strategy. Or maybe an 'insert' strategy (for open hashing).
		while self._table[i] != None and self._table[i].key() != key:
		 	i = (i + 1) % len(self._table)
		if (self._table[i] == None):
			# Adding a new entry
 			self._numEntries += 1
 		self._table[ i] = Entry(key,value)
	def has(self, key):
		hc = self._hashcode(key)
		i = hc % len(self._table)
		orig_i = i
		wrapped = False
		# TODO: pluggable probe strategy
		while self._table[i] != None and self._table[i].key() != key and not wrapped:
			i = (i + 1) % len(self._table)
			if (i == orig_i):
				wrapped = True
		if (self._table[i] == None or wrapped):
			retval = False
		else:
			retval = True
			return retval
	
	def get(self, key):
		"""Returns the value previously stored with put."""
		hc = self._hashcode(key)
		i = hc % len(self._table)
		orig_i = i
		wrapped = False
		# TODO: pluggable probe strategy
		while self._table[i] != None and self._table[i].key() != key and not wrapped:
			i = (i + 1) % len(self._table)
			if (i == orig_i):
				wrapped = True
		if (self._table[i] == None or wrapped):
			retval = None
		else:
			retval = self._table[i].value()
		return retval

	def entries(self):
		"""Returns all entries contained in this hashtable, in no particular order."""
		return self._table

	def count(self):
		return self._numEntries
# ---------------------------------------------- private functions -----------------------------------------------
	def _grow(self):
		"""Grows the array and rehashes everything."""
		#print( "\tgrow", file=sys.stderr)
		# print( "{0} grow".format("-" * 64))
		tablen = len(self._table) * 2
		newTable = [None] * tablen
		oldTable = self._table
		self._table = newTable
		self._numEntries = 0
		for entry in oldTable:
			# print( "grow: Entry: {0}".format(entry))
			if (entry == None):
				pass
			else:
				self.put(entry.key(), entry.value())
		# print( "{0} grow done".format("-" * 64))

	def _hashcode(self,key):
		"""Returns a hashcode for the given key."""
		# Probably doesn't need to be an instance method.
		if (type(key) is str):
			return ord( key[0]) if len(key) > 0 else 0
		else:
			return 0
# ------------------------------------------------------ Entry -------------------------------------------------------
class Entry():
	def __init__(self, aKey, aValue):
		self._key = aKey
		self._value = aValue

	def key(self):
		return self._key

	def value(self):
		return self._value
