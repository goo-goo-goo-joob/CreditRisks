using System;
using System.Collections.Generic;
using System.Linq;
using CreditMath;
using Xunit;

namespace CreditTests
{
    public class CMathTest
    {
        public static IEnumerable<object[]> GetWinsorizationData(int numTests)
        {
            // value, let, right, expected
            var allData = new List<object[]>
            {
                new object[] {-1, 0, 100, 0},
                new object[] {50, 0, 100, 50},
                new object[] {101, 0, 100, 100},
                new object[] {0, float.NegativeInfinity, float.PositiveInfinity, -1},
            };

            return allData.Take(numTests);
        }

        [Theory]
        [MemberData(nameof(GetWinsorizationData), parameters: 4)]
        public void WinsorizationCheck(float value, float left, float right, float expected)
        {
            float result = CMath.Winsorization(value, left, right);
            Assert.Equal(expected, result);
        }
    }
}