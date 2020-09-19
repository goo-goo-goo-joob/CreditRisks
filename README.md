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

# Запуск приложения

1. Собрать docker images (автоматизировано в CI)
```bash
docker build -t $APP_NAME --file Dockerfile .
```
2. Описать переменные окружения
```bash
# Адрес, на котором выполняет прослушивание ASPNETCORE сервер
ASPNETCORE_URLS=http://+:8080

# Порт, на котором работает python backend
LISTEN_PORT=9000

# Адрес для подключения к python backend
PYTHON_BACKEND_ADDR=python-app:9000

# Количество используемых ядер (по умолчанию все) 
PROCESS_COUNT=2

# Пудь до моделей внутри контейнера
MODEL_PATH=/usr/src/app/models/
```
3. Добавить модели на сервер, настроить файл [docker-compose.yml](docker-compose.yml)
4. Запустить
```bash
docker-compose up -d
```

# License
© @AsciiShell (Aleksey Podchezertsev), 
  @goo-goo-goo-joob (Mariia Samodelkina), 
  @andrsolo21 (Andrey Solodyankin),
  @apremizova (Anna Remizova), 2020. 
Licensed under the Apache License, Version 2.0. See LICENSE file for more details.
