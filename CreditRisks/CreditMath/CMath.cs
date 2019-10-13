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

        public static float Sigmoid(float value)
        {
            return (float) (1.0F / (1.0F + Math.Exp(-value)));
        }

        public static float Calibration(float value, float alpha, float beta)
        {
            return (float) Math.Min(1F, Math.Exp(alpha * value + beta));
        }
    }
}