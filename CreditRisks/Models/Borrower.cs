using System.ComponentModel.DataAnnotations;

namespace CreditRisks.Models
{
    public class Borrower
    {
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
    }
}