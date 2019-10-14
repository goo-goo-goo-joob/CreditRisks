using System;
using System.Collections.Generic;
using System.Linq;
using CreditMath;
using Xunit;

namespace CreditTests
{
    public class CMathTest
    {
        [Theory]
        [InlineData(-1, 0, 100, 0)]
        [InlineData(50, 0, 100, 50)]
        [InlineData(101, 0, 100, 100)]
        [InlineData(0, float.NegativeInfinity, float.PositiveInfinity, 0)]
        public void WinsorizationCheck(float value, float left, float right, float expected)
        {
            float result = CMath.Winsorization(value, left, right);
            Assert.Equal(expected, result);
        }

        [Theory]
        [InlineData(100, 0, 1, 100)]
        [InlineData(200, 0, 100, 2)]
        [InlineData(200, 100, 200, 1)]
        public void MinMaxNormCheck(float value, float left, float right, float expected)
        {
            float result = CMath.MinMaxNorm(value, left, right);
            Assert.Equal(expected, result);
        }

        [Theory]
        [InlineData(0, 0.5F)]
        [InlineData(10, 1)]
        [InlineData(-10, 0)]
        [InlineData(2, 0.88079707797)]
        [InlineData(-2, 0.11920292202)]
        public void SigmoidCheck(float value, float expected)
        {
            float result = CMath.Sigmoid(value);
            Assert.Equal(expected, result, 4);
        }
    }
}