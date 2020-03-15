# CreditRisks #19029 Программный модуль для управления кредитными рисками банка

[Website](http://credit-risks.asciishell.ru/)

[![Build Status](https://travis-ci.com/goo-goo-goo-joob/CreditRisks.svg?token=eht78Z7mqWPNCUpFTSub&branch=master)](https://travis-ci.com/goo-goo-goo-joob/CreditRisks)

Проект #19029 Программный модуль для управления кредитными рисками банка.

[PythonBackend](/PythonBackend) - Python backend для обработки запросов на вычисления вероятности дефолта конкретного запроса.

[CreditRisks](/CreditRisks) - Frontend на .Net Core для отображения пользовательского интерфейса, обработки входящих http запросов.

[metrics_library](/metrics_library) - Реализация метрики прибыли и других графических инструментов.

[notebooks](/notebooks) - основные jupyter ноутбуки для обработки данных.

[bankrupt_crawler](/bankrupt_crawler) - Описание бота для сбора данных с платформы [fedresurs](/https://bankrot.fedresurs.ru/).

# Прочие файлы

`.travis.yml` - настройка CI; запускает тесты, линтеры, выполняет сборку docker контейнеров и отправляет их в хранилище.

`Makefile` - содержит инструкции для CI

`calc_service.proto` - Protobuf файл, описывающий взаимодействия частей приложения, написанных на .Net Core и python

# Порядок работы

При создании коммита в ветке master или в теге создается сборка, которая отправит готовый образ в хранилище в случае успеха.
На сервере запускаются контейнеры приложений с настоенными переменными окружения.
Все HTTP запросы обрабатываются .Net Core приложением, данные на python передаются по протоколу grpc, где далее происходят вычисления.
