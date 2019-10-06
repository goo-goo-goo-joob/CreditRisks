using System;

namespace CreditMath
{
    public abstract class CMath
    {
        public static float Winsorization(float value, float left, float right)
        {
            if (value > right)
                return right;
            if (value < left)
                return left;
            return value;
        }

        public static float MinMaxNorm(float value, float left, float right)
        {
            return (value - left) / (right - left);
        }
    }
}