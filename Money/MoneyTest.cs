using System;
using System.Collections.Generic;
using System.Text;
using NUnit.Framework;

namespace Money
{
    [TestFixture]
    public class MoneyTest
    {
        [Test]
        public void Multiplication()
        {
            Money five = Money.MakeDollar(5);
            Assert.AreEqual(Money.MakeDollar(10), five.Times(2));
            Assert.AreEqual(Money.MakeDollar(15), five.Times(3));
        }

        [Test]
        public void Equality()
        {
            Assert.IsTrue(Money.MakeDollar(5).Equals(Money.MakeDollar(5)));
            Assert.IsFalse(Money.MakeDollar(5).Equals(Money.MakeDollar(6)));
            Assert.IsFalse(Money.MakeFranc(5).Equals(Money.MakeDollar(5)));
        }

        [Test]
        public void Currency()
        {
            Assert.AreEqual("USD", Money.MakeDollar(1).Currency);
            Assert.AreEqual("CHF", Money.MakeFranc(1).Currency);
        }

        [Test]
        public void SimpleAddition()
        {
            Money five = Money.MakeDollar(5);
            Expression sum = five.Plus(five);
            Bank bank = new Bank();
            Money reduced = bank.Reduce(sum, "USD");
            Assert.AreEqual(Money.MakeDollar(10), reduced);
        }


        [Test]
        public void PlusReturnsSum()
        {
            Money five = Money.MakeDollar(5);
            Expression result = five.Plus(five);
            Sum sum = (Sum)result;
            Assert.AreEqual(five, sum.augend);
            Assert.AreEqual(five, sum.addend);
        }

        [Test]
        public void ReduceSum()
        {
            Expression sum = new Sum(Money.MakeDollar(3), Money.MakeDollar(4));
            Bank bank = new Bank();
            Money result = bank.Reduce(sum, "USD");
            Assert.AreEqual(Money.MakeDollar(7), result);
        }

        [Test]
        public void ReduceMoney()
        {
            Bank bank = new Bank();
            Money result = bank.Reduce(Money.MakeDollar(1), "USD");
            Assert.AreEqual(Money.MakeDollar(1), result);
        }

        [Test]
        public void ReduceMoneyDifferentCurrency()
        {
            Bank bank = new Bank();
            bank.AddRate("CHF", "USD", 2);
            Money result = bank.Reduce(Money.MakeFranc(2), "USD");
            Assert.AreEqual(Money.MakeDollar(1), result);
        }

        [Test]
        public void IdentityRate()
        {
            Assert.AreEqual(1, new Bank().Rate("USD", "USD"));
        }

        [Test]
        public void MixedAddition()
        {
            Expression fiveBucks = Money.MakeDollar(5);
            Expression tenFrancs = Money.MakeFranc(10);
            Bank bank = new Bank();
            bank.AddRate("CHF", "USD", 2);
            Money result = bank.Reduce(fiveBucks.Plus(tenFrancs), "USD");
            Assert.AreEqual(Money.MakeDollar(10), result);
        }

        [Test]
        public void SumPlusMoney()
        {
            Expression fiveBucks = Money.MakeDollar(5);
            Expression tenFrancs = Money.MakeFranc(10);
            Bank bank = new Bank();
            bank.AddRate("CHF", "USD", 2);
            Expression sum = new Sum(fiveBucks, tenFrancs).Plus(fiveBucks);
            Money result = bank.Reduce(sum, "USD");
            Assert.AreEqual(Money.MakeDollar(15), result);
        }

        [Test]
        public void SumTimes()
        {
            Expression fiveBucks = Money.MakeDollar(5);
            Expression tenFrancs = Money.MakeFranc(10);
            Bank bank = new Bank();
            bank.AddRate("CHF", "USD", 2);
            Expression sum = new Sum(fiveBucks, tenFrancs).Times(2);
            Money result = bank.Reduce(sum, "USD");
            Assert.AreEqual(Money.MakeDollar(20), result);
        }
    }
}
