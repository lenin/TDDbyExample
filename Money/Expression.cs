using System;
using System.Collections.Generic;
using System.Text;

namespace Money
{
    public interface Expression
    {
        Money Reduce(Bank bank, string to);
        Expression Plus(Expression addend);
        Expression Times(int multiplier);
    }
}
