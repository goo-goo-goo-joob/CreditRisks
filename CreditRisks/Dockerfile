FROM mcr.microsoft.com/dotnet/core/sdk:2.2 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY CreditRisks/ .
COPY calc_service.proto .
RUN dotnet restore

# Copy everything else and build
WORKDIR /app/CreditRisks/CreditRisks
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:2.2
COPY --from=build-env /app/CreditRisks/CreditRisks/out .
ENTRYPOINT ["dotnet", "CreditRisks.dll"]