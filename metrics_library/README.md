# Metrics Library

### Доступные функции и методы:

`profits.plt_profit` -- Строит график метрики прибыли относительно порога разбиения

`profits.plt_profit_recall`  -- Строит график метрики прибыли относительно recall. Для сравнения так же может построить ROC на том же графике

`profits.plt_mcc` -- Строит график MCC относительно порога разбиения

`profits.plt_popularity` -- Строит график доли объектов ниже порога относительно порога разбиения

`Metrics.plt_fp` -- Строит график FPR относительно порога разбиения

`Metrics.plt_roc` -- Строит график ROC относительно порога разбиения

`rosstat_utils.plot_corr` -- Строит таблицу корреляции параметров датасета

### Константы

 `rosstat_utils` содержит список констант для работы с исходными данными датасетов Росстата

Пример использования

```python
from CreditRisks.metrics_library import profits

profits.plt_profit(target, predict)
```


<img src=https://user-images.githubusercontent.com/23531231/76706037-a9340200-66f5-11ea-8719-eb3958dfcf55.png width="300">