using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;

namespace CreditRisks.Models
{
    [SuppressMessage("ReSharper", "CommentTypo")]
    public class Company
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
        public bool OrganizationStructureRisk { get; set; }

        /// <summary>
        /// Положительная информация по составу акционеров
        /// </summary>
        public bool PositiveShareholders { get; set; }

        /// <summary>
        /// Отрицательная информация по составу акционеров
        /// </summary>
        public bool NegativeShareholders { get; set; }

        /// <summary>
        /// Желание/возможность вкладывать дополнительные средства в бизнес
        /// </summary>
        public bool DesireToInvest { get; set; }

        /// <summary>
        /// Изъятие собственником средств из бизнеса
        /// </summary>
        public bool WithdrawalFunds { get; set; }

        /// <summary>
        /// Наличие споров по доле в собственном капитале или активам компании между собственниками
        /// </summary>
        public bool OwnershipConflict { get; set; }

        /// <summary>
        /// Наличие конфликтов между руководством и акционерами компании
        /// </summary>
        public bool ManagementShareholdersConflict { get; set; }

        /// <summary>
        /// Продуктовая концентрация
        /// </summary>
        public bool ProductConcentration { get; set; }

        /// <summary>
        /// Наличие у компании нерыночных преимуществ, дающих особый статус или положение на рынке
        /// </summary>
        public bool NonMarketAdvantages { get; set; }

        /// <summary>
        /// Переговорная позиция с поставщиками
        /// </summary>
        public bool PositiveWithSuppliers { get; set; }

        /// <summary>
        /// Концентрация поставщиков
        /// </summary>
        public bool ConcentrationOfSuppliers { get; set; }

        /// <summary>
        /// Переговорная позиция с покупателями
        /// </summary>
        public bool PositiveWithBuyers { get; set; }

        /// <summary>
        /// Концентрация покупателей
        /// </summary>
        public bool ConcentrationOfBuyers { get; set; }

        /// <summary>
        /// Участие в финансировании сделки собственными средствами
        /// </summary>
        public bool OwnFundsTransaction { get; set; }

        /// <summary>
        /// Адекватность источников погашения
        /// </summary>
        public bool RelevantRepayment { get; set; }

        // Данные бух учета
    }
}