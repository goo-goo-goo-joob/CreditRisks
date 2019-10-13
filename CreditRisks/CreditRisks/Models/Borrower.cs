using System;
using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;
using CreditMath;
using static CreditMath.CMath;

namespace CreditRisks.Models
{
    [SuppressMessage("ReSharper", "CommentTypo")]
    public class Borrower
    {
        /// <summary>
        /// ИНН
        /// </summary>
        [StringLength(10, MinimumLength = 10)]
        public string INN { get; set; }

        /// <summary>
        /// Вероятность дефолта
        /// </summary>
        [Range(0, 1)]
        public float DefaultProbability { get; set; }

        #region Params

        // Нефинансовые показатели кредитного риска

        /// <summary>
        /// Макроэкономический риск
        /// </summary>
        [Range(0, 1)]
        public float MacroeconomicRisk { get; set; }

        /// <summary>
        /// Рейтинг отрасли
        /// </summary>
        [Range(1, 5)]
        public float IndustryRating { get; set; }

        /// <summary>
        /// Риск бизнес-модели
        /// </summary>
        [Range(0, 1)]
        public float BusinessModelRisk { get; set; }

        /// <summary>
        /// Риск организацнонной структуры
        /// </summary>
        [Range(-1, 1)]
        public float OrganizationStructureRisk { get; set; }

        /// <summary>
        /// Положительная информация по составу акционеров
        /// </summary>
        [Range(0, 1)]
        public float PositiveShareholders { get; set; }

        /// <summary>
        /// Отрицательная информация по составу акционеров
        /// </summary>
        [Range(-1, 0)]
        public float NegativeShareholders { get; set; }

        /// <summary>
        /// Желание/возможность вкладывать дополнительные средства в бизнес
        /// </summary>
        [Range(0, 1)]
        public float DesireToInvest { get; set; }

        /// <summary>
        /// Изъятие собственником средств из бизнеса
        /// </summary>
        [Range(-1, 0)]
        public float WithdrawalFunds { get; set; }

        /// <summary>
        /// Наличие споров по доле в собственном капитале или активам компании между собственниками
        /// </summary>
        [Range(-1, 0)]
        public float OwnershipConflict { get; set; }

        /// <summary>
        /// Наличие конфликтов между руководством и акционерами компании
        /// </summary>
        [Range(-1, 0)]
        public float ManagementShareholdersConflict { get; set; }

        /// <summary>
        /// Продуктовая концентрация
        /// </summary>
        [Range(-1, 1)]
        public float ProductConcentration { get; set; }

        /// <summary>
        /// Наличие у компании нерыночных преимуществ, дающих особый статус или положение на рынке
        /// </summary>
        [Range(-1, 0)]
        public float NonMarketAdvantages { get; set; }

        /// <summary>
        /// Переговорная позиция с поставщиками
        /// </summary>
        [Range(-1, 1)]
        public float PositiveWithSuppliers { get; set; }

        /// <summary>
        /// Концентрация поставщиков
        /// </summary>
        [Range(-1, 1)]
        public float ConcentrationOfSuppliers { get; set; }

        /// <summary>
        /// Переговорная позиция с покупателями
        /// </summary>
        [Range(-1, 1)]
        public float PositiveWithBuyers { get; set; }

        /// <summary>
        /// Концентрация покупателей
        /// </summary>
        [Range(-1, 1)]
        public float ConcentrationOfBuyers { get; set; }

        /// <summary>
        /// Участие в финансировании сделки собственными средствами
        /// </summary>
        [Range(-1, 1)]
        public float OwnFundsTransaction { get; set; }

        /// <summary>
        /// Адекватность источников погашения
        /// </summary>
        [Range(-1, 1)]
        public float RelevantRepayment { get; set; }

        // Финансовые показатели кредитного риска

        /// <summary>
        /// Кредитноеое плечо
        /// </summary>
        public float CreditLeverage { get; set; }

        /// <summary>
        /// Финансовая независимость
        /// </summary>
        public float FinancialIndependence { get; set; }

        /// <summary>
        /// Долговая нагрузка
        /// </summary>
        public float DebtBurden { get; set; }

        /// <summary>
        /// Покрытие финансового долга накопленной прибылью
        /// </summary>
        public float CoverageDebtWithAccumulatedProfit { get; set; }

        /// <summary>
        /// Рентабельность активов по чистой прибыли
        /// </summary>
        public float ReturnAssetsNetProfit { get; set; }

        /// <summary>
        /// Рентабельность активов по операционной прибыли
        /// </summary>
        public float ReturnAssetsOperatingProfit { get; set; }

        /// <summary>
        /// операционная рентабельность
        /// </summary>
        public float OperatingMargin { get; set; }

        /// <summary>
        /// рентабельность деятельности по чистой прибыли
        /// </summary>
        public float NetProfitMargin { get; set; }

        /// <summary>
        /// покрытие обязательств операционной прибылью
        /// </summary>
        public float LiabilityCoverageOperatingProfit { get; set; }

        /// <summary>
        /// соотношение операционной прибыли и финансового долга
        /// </summary>
        public float OperatingProfitFinancialDebtRatio { get; set; }

        /// <summary>
        /// соотношение финансового долга и выручки
        /// </summary>
        public float FinancialDebtRevenueRatio { get; set; }

        /// <summary>
        /// текущая ликвидность
        /// </summary>
        public float CurrentLiquidity { get; set; }

        /// <summary>
        /// быстрая ликвидность
        /// </summary>
        public float QuickLiquidity { get; set; }

        /// <summary>
        /// мгновенная ликвидность
        /// </summary>
        public float InstantLiquidity { get; set; }

        /// <summary>
        /// уровень работающих активов
        /// </summary>
        public float LevelOfOperatingAssets { get; set; }

        /// <summary>
        /// финансовый цикл
        /// </summary>
        public float FinancialCycle { get; set; }

        /// <summary>
        /// оборачиваемость активов
        /// </summary>
        public float AssetTurnover { get; set; }

        #endregion

        public Borrower(Company company)
        {
            float financialDebt = company.Code_15003 + company.Code_14003 - company.Code_12503;
            this.INN = company.INN;
            this.DefaultProbability = company.DefaultProbability;
            this.MacroeconomicRisk = company.MacroeconomicRisk;
            this.IndustryRating = company.IndustryRating;
            this.BusinessModelRisk = company.BusinessModelRisk;
            this.OrganizationStructureRisk = company.OrganizationStructureRisk;
            this.PositiveShareholders = company.PositiveShareholders;
            this.NegativeShareholders = company.NegativeShareholders;
            this.DesireToInvest = company.DesireToInvest;
            this.WithdrawalFunds = company.WithdrawalFunds;
            this.OwnershipConflict = company.OwnershipConflict;
            this.ManagementShareholdersConflict = company.ManagementShareholdersConflict;
            this.ProductConcentration = company.ProductConcentration;
            this.NonMarketAdvantages = company.NonMarketAdvantages;
            this.PositiveWithSuppliers = company.PositiveWithSuppliers;
            this.ConcentrationOfSuppliers = company.ConcentrationOfSuppliers;
            this.PositiveWithBuyers = company.PositiveWithBuyers;
            this.ConcentrationOfBuyers = company.ConcentrationOfBuyers;
            this.OwnFundsTransaction = company.OwnFundsTransaction;
            this.RelevantRepayment = company.RelevantRepayment;
            this.CreditLeverage = company.Code_13003 / company.Code_15003;
            this.FinancialIndependence = company.Code_13003 / company.Code_16003;
            this.DebtBurden = financialDebt / company.Code_16003;
            this.CoverageDebtWithAccumulatedProfit = company.Code_13003 / financialDebt;
            this.ReturnAssetsNetProfit = company.Code_24003 / company.Code_16003;
            this.ReturnAssetsOperatingProfit = company.Code_22003 / company.Code_16003;
            this.OperatingMargin = company.Code_22003 / Math.Max(company.Code_21103, financialDebt);
            this.NetProfitMargin = company.Code_24003 / Math.Max(company.Code_21103, financialDebt);
            this.LiabilityCoverageOperatingProfit = company.Code_22003 / (company.Code_14003 + company.Code_15003);
            this.OperatingProfitFinancialDebtRatio = company.Code_22003 / financialDebt;
            this.FinancialDebtRevenueRatio = financialDebt / company.Code_21103;
            this.CurrentLiquidity = company.Code_12003 / company.Code_15003;
            this.QuickLiquidity = (company.Code_12003 - company.Code_12103) / company.Code_15003;
            this.InstantLiquidity = company.Code_12503 / company.Code_15003;
            this.LevelOfOperatingAssets = (company.Code_12103 + company.Code_12303 - company.Code_15203) / company.Code_21103;
            float turnoverDebtorDebt = 365 * (company.Code_12303 + company.Code_12304) / (2 * company.Code_21103);
            float turnoverReserves = 365 * (company.Code_12103 + company.Code_12104) / (2 * company.Code_21103);
            float turnoverCreditDebt = 365 * (company.Code_15203 + company.Code_15204) / (2 * company.Code_21103);
            this.FinancialCycle = turnoverDebtorDebt + turnoverReserves - turnoverCreditDebt;
            this.AssetTurnover = company.Code_21103 / company.Code_16003;
        }

        public WeightTuple MacroeconomicRiskP = new WeightTuple {Weight = -2.18F};
        public WeightTuple IndustryRatingP = new WeightTuple {Weight = -0.393F, NormLeft = 2, NormRight = 3};
        public WeightTuple BusinessModelRiskP = new WeightTuple {Weight = -0.656F};

        public WeightTuple ReturnAssetsNetProfitP = new WeightTuple
        {
            Weight = -0.379F, NormLeft = 0.001F, NormRight = 0.025F, WinsLeft = -0.049F, WinsRight = 0.082F,
        };

        public WeightTuple FinancialDebtRevenueRatioP = new WeightTuple
        {
            Weight = -0.369F, NormLeft = 0.322F, NormRight = 2.684F, WinsRight = 3.842F, Transform = f => (float) Math.Log(f + 0.0001F),
        };

        public WeightTuple InstantLiquidityP = new WeightTuple
        {
            Weight = -0.734F, NormLeft = 0.002F, NormRight = 0.048F, WinsRight = 0.068F,
        };

        public WeightTuple ManagementsScoreP = new WeightTuple
        {
            Weight = -0.371F, NormRight = 0.167F, WinsRight = 0.068F,
        };

        public WeightTuple DealRatioP = new WeightTuple {Weight = -0.812F,};

        public const float Bias = 0.257F;

        public float CalcDefault()
        {
            float sum = Bias;
            sum += MacroeconomicRiskP.Calc(MacroeconomicRisk);
            sum += IndustryRatingP.Calc(IndustryRating);
            sum += BusinessModelRiskP.Calc(BusinessModelRisk);
            sum += ReturnAssetsNetProfitP.Calc(ReturnAssetsNetProfit);
            sum += FinancialDebtRevenueRatioP.Calc(FinancialDebtRevenueRatio);
            sum += InstantLiquidityP.Calc(InstantLiquidity);
            float managementScoreSum = (PositiveShareholders +
                                        NegativeShareholders +
                                        DesireToInvest +
                                        WithdrawalFunds +
                                        OwnershipConflict +
                                        ManagementShareholdersConflict) / 6;
            sum += ManagementsScoreP.Calc(managementScoreSum);
            float dealRatioSum = (OwnFundsTransaction +
                                  RelevantRepayment) / 2;
            sum += DealRatioP.Calc(dealRatioSum);
            return Calibration(Sigmoid(sum), 0.528F, -1.014F) * 100.0F;
        }
    }
}