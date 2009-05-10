import unittest

from money import Money, Bank, Sum

class MoneyTestCase(unittest.TestCase):
	def testMultiplication(self):
		five = Money.dollar(5)
		self.assertEquals(Money.dollar(10), five.times(2))
		self.assertEquals(Money.dollar(15), five.times(3))
	
	def testEquality(self):
		self.assertTrue(Money.dollar(5) == Money.dollar(5))
		self.assertFalse(Money.dollar(5) == Money.dollar(6))
		self.assertFalse(Money.franc(5) == Money.dollar(5))
	
	def testCurrency(self):
		self.assertEquals('USD', Money.dollar(1).currency)
		self.assertEquals('CHF', Money.franc(1).currency)
	
	def testSimpleAddition(self):
		five = Money.dollar(5)
		sum = five.plus(five)
		bank = Bank()
		reduced = bank.reduce(sum, 'USD')
		self.assertEquals(Money.dollar(10), reduced)
	
	def testPlusReturnsSum(self):
		five = Money.dollar(5)
		sum = five.plus(five)
		self.assertEquals(five, sum.augend)
		self.assertEquals(five, sum.addend)
	
	def testReduceSum(self):
		sum = Sum(Money.dollar(3), Money.dollar(4))
		bank = Bank()
		result = bank.reduce(sum, 'USD')
		self.assertEquals(Money.dollar(7), result)
	
	def testReduceMoney(self):
		bank = Bank()
		result = bank.reduce(Money.dollar(1), 'USD')
		self.assertEquals(Money.dollar(1), result)
	
	def testReduceMoneyDifferentCurrency(self):
		bank = Bank()
		bank.addRate('CHF', 'USD', 2)
		result = bank.reduce(Money.franc(2), 'USD')
		self.assertEquals(Money.dollar(1), result)
	
	def testTupleEquals(self):
		self.assertEquals(('USD', 'CHF'), ('USD', 'CHF'))
	
	def testIdentityRate(self):
		self.assertEquals(1, Bank().rate('USD', 'USD'))
	
	def testMixedAddition(self):
		fiveBucks = Money.dollar(5)
		tenFrancs = Money.franc(10)
		bank = Bank()
		bank.addRate('CHF', 'USD', 2)
		result = bank.reduce(fiveBucks.plus(tenFrancs), 'USD')
		self.assertEquals(Money.dollar(10), result)
	
	def testSumPlusMoney(self):
		fiveBucks = Money.dollar(5)
		tenFrancs = Money.franc(10)
		bank = Bank()
		bank.addRate('CHF', 'USD', 2)
		sum = Sum(fiveBucks, tenFrancs).plus(fiveBucks)
		result = bank.reduce(sum, 'USD')
		self.assertEquals(Money.dollar(15), result)
	
	def testSumTimes(self):
		fiveBucks = Money.dollar(5)
		tenFrancs = Money.franc(10)
		bank = Bank()
		bank.addRate('CHF', 'USD', 2)
		sum = Sum(fiveBucks, tenFrancs).times(2)
		result = bank.reduce(sum, 'USD')
		self.assertEquals(Money.dollar(20), result)

if __name__ == "__main__":
	unittest.main()
