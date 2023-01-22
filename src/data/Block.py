from array import array
from src.lib.buffer import buffer
from src.lib.crypto.sha256 import sha256, EMPTY_HASH_SHA256

EMPTY_HASH = buffer(EMPTY_HASH_SHA256)

class Block:
	invalid: bool = False
	version: int = 1
	index: int = 0
	time: int = 0
	anchor: buffer = EMPTY_HASH
	countOfTransactions: int = 0
	listOfTransactions: list[buffer] = []

	#region Get/Set
	
	def getVersion(self): return self.version
	def setVersion(self, value: int):
		self.version = value
		return self

	def getIndex(self): return self.index
	def setIndex(self, value: int):
		self.index = value
		return self

	def getTime(self): return self.time
	def setTime(self, value: int):
		self.time = value
		return self

	def getAnchor(self): return self.anchor
	def setAnchor(self, value: int):
		self.anchor = value
		return self

	def getCountOfTransactions(self): return self.countOfTransactions
	def addTransaction(self, txn: buffer):
		self.listOfTransactions.append(txn)
		self.listOfTransactions = sorted(self.listOfTransactions)
		self.countOfTransactions += 1

	#endregion Get/Set
	#region Buffer

	def readBuffer(self, buffer: buffer):
		try:
			self.version = buffer.readUleb128()
			self.index = buffer.readUleb128()
			self.time = buffer.readUleb128()
			self.anchor = buffer.readBlob(32)
			self.countOfTransactions = buffer.readUleb128()
			self.listOfTransactions = []
			i = self.countOfTransactions
			while i > 0:
				i -= 1
				self.listOfTransactions.append(buffer.readBlob())
			self.listOfTransactions = sorted(self.listOfTransactions)
		except:
			self.invalid = True

		return self
	
	@staticmethod
	def fromBuffer(buffer: buffer):
		return Block().readBuffer(buffer)

	@staticmethod
	def fromBytes(bytearray: bytes | bytearray | buffer):
		return Block().readBuffer(buffer(bytearray))

	@staticmethod
	def fromHex(hex: str):
		return Block().readBuffer(buffer.fromHex(hex))

	def toBuffer(self) -> buffer:
		result = buffer.concat([
			buffer.encodeLeb128(self.version),
			buffer.encodeLeb128(self.index),
			buffer.encodeLeb128(self.time),
			self.anchor,
			buffer.encodeLeb128(self.countOfTransactions)
		])
	
		for txn in self.listOfTransactions:
			result += buffer.encodeLeb128(len(txn))
			result += txn
		return result

	def getHash(self):
		return sha256(self.toBuffer())

	#endregion Buffer
	#region Magic

	def __iter__(self):
		return self.listOfTransactions

	def __str__(self) -> str:
		if self.invalid:
			return "<Block !>"
		else:
			result = "<Block"
			result += "\n  version="+ str(self.version)
			result += "  index="+ str(self.index)
			result += "  time="+ str(self.time)
			result += "  txns="+ str(self.countOfTransactions)
			result += "\n  anchor="+ self.anchor.toHex()
			for txn in self.listOfTransactions:
				result += "\n  "+ txn.toHex()
			result += "\n>"
			return result

	#endregion Magic

buf = buffer.fromHex('01'+'01'+'01'+'e63bb9f57a5e2d4c66c3f72b9a9f2ebebd2c0e2900f19afae09ccebea6f0c3ec'+'03'+'06eeeeeeeeeeee'+'05ffffffffff'+'05aaaaaaaaaa')
print(buf)
block = Block.fromBuffer(buf)
print(block)
print(block.toBuffer())