class Money:
	def __init__(self, amount, currency):
		self.amount = amount
		self.currency = currency
	
	def __eq__(self, other):
		return self.amount == other.amount \
			and self.currency == other.currency
	
	def __repr__(self):
		return "<%s %s>" % (self.amount, self.currency)
	
	@classmethod
	def dollar(cls, amount):
		return Money(amount, 'USD')
	
	@classmethod
	def franc(cls, amount):
		return Money(amount, 'CHF')
	
	def times(self, multiplier):
		return Money(self.amount * multiplier, self.currency)
	
	def plus(self, addend):
		return Sum(self, addend)
	
	def reduce(self, bank, to):
		return Money(self.amount / bank.rate(self.currency, to), to)

class Bank:
	def __init__(self):
		self.rates = {}

	def reduce(self, source, to):
		return source.reduce(self, to)
	
	def addRate(self, from_currency, to_currency, rate):
		self.rates[(from_currency, to_currency)] = rate
	
	def rate(self, from_currency, to_currency):
		if (from_currency == to_currency):
			return 1
		return self.rates[(from_currency, to_currency)]

class Sum:
	def __init__(self, augend, addend):
		self.augend = augend
		self.addend = addend

	def times(self, multiplier):
		return Sum(self.augend.times(multiplier), self.addend.times(multiplier))
	
	def plus(self, addend):
		return Sum(self, addend)
	
	def reduce(self, bank, to):
		amount = self.augend.reduce(bank, to).amount + self.addend.reduce(bank, to).amount
		return Money(amount, to)
