using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;

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
    }
}