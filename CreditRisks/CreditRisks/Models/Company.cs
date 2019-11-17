using System.Collections.Generic;
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
        public Dictionary<string, string> DefaultProbability { get; set; }
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
        public int BusinessModelRisk { get; set; }

        /// <summary>
        /// Риск организацнонной структуры
        /// </summary>
        public int OrganizationStructureRisk { get; set; }

        /// <summary>
        /// Положительная информация по составу акционеров
        /// </summary>
        public int PositiveShareholders { get; set; }

        /// <summary>
        /// Отрицательная информация по составу акционеров
        /// </summary>
        public int NegativeShareholders { get; set; }

        /// <summary>
        /// Желание/возможность вкладывать дополнительные средства в бизнес
        /// </summary>
        public int DesireToInvest { get; set; }

        /// <summary>
        /// Изъятие собственником средств из бизнеса
        /// </summary>
        public int WithdrawalFunds { get; set; }

        /// <summary>
        /// Наличие споров по доле в собственном капитале или активам компании между собственниками
        /// </summary>
        public int OwnershipConflict { get; set; }

        /// <summary>
        /// Наличие конфликтов между руководством и акционерами компании
        /// </summary>
        public int ManagementShareholdersConflict { get; set; }

        /// <summary>
        /// Продуктовая концентрация
        /// </summary>
        public int ProductConcentration { get; set; }

        /// <summary>
        /// Наличие у компании нерыночных преимуществ, дающих особый статус или положение на рынке
        /// </summary>
        public int NonMarketAdvantages { get; set; }

        /// <summary>
        /// Переговорная позиция с поставщиками
        /// </summary>
        public int PositiveWithSuppliers { get; set; }

        /// <summary>
        /// Концентрация поставщиков
        /// </summary>
        public int ConcentrationOfSuppliers { get; set; }

        /// <summary>
        /// Переговорная позиция с покупателями
        /// </summary>
        public int PositiveWithBuyers { get; set; }

        /// <summary>
        /// Концентрация покупателей
        /// </summary>
        public int ConcentrationOfBuyers { get; set; }

        /// <summary>
        /// Участие в финансировании сделки собственными средствами
        /// </summary>
        public int OwnFundsTransaction { get; set; }

        /// <summary>
        /// Адекватность источников погашения
        /// </summary>
        public int RelevantRepayment { get; set; }

        // Данные бух учета
        /// <summary>
        /// Запасы
        /// </summary>
        public float Code_12103 { get; set; }

        /// <summary>
        /// Запасы - на 31 декабря предыдущего года
        /// </summary>
        public float Code_12104 { get; set; }

        /// <summary>
        /// Дебиторская задолженность
        /// </summary>
        public float Code_12303 { get; set; }

        /// <summary>
        /// Дебиторская задолженность - на 31 декабря предыдущего года
        /// </summary>
        public float Code_12304 { get; set; }

        /// <summary>
        /// Денежные средства и денежные эквиваленты
        /// </summary>
        public float Code_12503 { get; set; }

        /// <summary>
        /// Итого оборотных активов
        /// </summary>
        public float Code_12003 { get; set; }

        /// <summary>
        /// Баланс
        /// </summary>
        public float Code_16003 { get; set; }

        /// <summary>
        /// Итого капитала и резервов
        /// </summary>
        public float Code_13003 { get; set; }

        /// <summary>
        /// Итого долгосрочных обязательств
        /// </summary>
        public float Code_14003 { get; set; }

        /// <summary>
        /// Кредиторская задолженность
        /// </summary>
        public float Code_15203 { get; set; }

        /// <summary>
        /// Кредиторская задолженность - на 31 декабря предыдущего года
        /// </summary>
        public float Code_15204 { get; set; }

        /// <summary>
        /// Итого краткосрочных обязательств
        /// </summary>
        public float Code_15003 { get; set; }

        /// <summary>
        /// Чистая прибыль (убыток) - за последние 4 квартала
        /// </summary>
        public float Code_24003 { get; set; }

        /// <summary>
        /// Прибыль (убыток) от продаж - за последние 4 квартала
        /// </summary>
        public float Code_22003 { get; set; }

        /// <summary>
        /// Выручка - за последние 4 квартала
        /// </summary>
        public float Code_21103 { get; set; }
    }
}