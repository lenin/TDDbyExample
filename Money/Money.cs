using System;
using System.Collections.Generic;
using System.Text;

namespace Money
{
    public class Money : Expression
    {
        public int amount;
        protected string currency;

        public Money(int amount, string currency)
        {
            this.amount = amount;
            this.currency = currency;
        }

        public string Currency
        {
            get { return currency; }
        }

        public Expression Times(int multiplier) {
            return new Money(amount * multiplier, currency);
        }

        public Expression Plus(Expression addend)
        {
            return new Sum(this, addend);
        }

        public Money Reduce(Bank bank, string to)
        {
            int rate = bank.Rate(currency, to);
            return new Money(amount / rate, to);
        }

        public override bool Equals(object obj)
        {
            Money money = (Money)obj;
            return amount == money.amount
                && Currency == money.Currency;
        }

        public override string ToString()
        {
            return amount + " " + currency;
        }

        public static Money MakeDollar(int amount)
        {
            return new Money(amount, "USD");
        }

        public static Money MakeFranc(int amount)
        {
            return new Money(amount, "CHF");
        }
    }
}
