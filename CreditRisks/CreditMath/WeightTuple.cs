using System;

namespace CreditMath
{
    public class WeightTuple
    {
        public float WinsLeft = float.NegativeInfinity;
        public float WinsRight = float.PositiveInfinity;
        public Func<float, float> Transform = f => f;
        public float NormLeft = 0;
        public float NormRight = 1;
        public float Weight = 0;

        public float Calc(float value)
        {
            return Weight * CMath.MinMaxNorm(Transform(CMath.Winsorization(value, WinsLeft, WinsRight)), NormLeft, NormRight);
        }
    }
}