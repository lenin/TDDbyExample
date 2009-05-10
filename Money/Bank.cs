using System;
using System.Collections.Generic;
using System.Text;

namespace Money
{
    public class Bank
    {
        private Dictionary<Pair, int> rates = new Dictionary<Pair, int>();

        public void AddRate(string from, string to, int rate)
        {
            rates.Add(new Pair(from, to), rate);
        }

        public int Rate(string from, string to)
        {
            if (from == to) return 1;
            return rates[new Pair(from, to)];
        }

        public Money Reduce(Expression source, string to)
        {
            return source.Reduce(this, to);
        }

        private class Pair
        {
            private string from;
            private string to;

            public Pair(string from, string to)
            {
                this.from = from;
                this.to = to;
            }

            public override bool Equals(object obj)
            {
                Pair pair = (Pair)obj;
                return from == pair.from && to == pair.to;
            }

            public override int GetHashCode()
            {
                return 0;
            }
        }
    }
}
