FROM mcr.microsoft.com/dotnet/core/sdk:2.2 AS build-env
WORKDIR /app

COPY . .

WORKDIR /app/CreditRisks
RUN dotnet restore

WORKDIR /app/CreditRisks/CreditRisksRestAPI
RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/core/aspnet:2.2
COPY --from=build-env /app/CreditRisks/CreditRisksRestAPI/out .
ENTRYPOINT ["dotnet", "CreditRisksRestAPI.dll"]