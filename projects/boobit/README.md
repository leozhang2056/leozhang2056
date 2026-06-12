# Boobit

## Overview

Boobit is a cryptocurrency trading platform mobile application that enables users to query market data, search for coins, and perform exchange and recharge operations.

## Features

- **Market Query**: Real-time cryptocurrency price tracking and market data visualization
- **Search**: Advanced search functionality for discovering and filtering cryptocurrencies
- **Exchange**: Currency conversion and trading capabilities
- **Recharge**: Deposit and wallet funding operations
- **Wallet Management**: Secure digital asset storage and transaction history

## Tech Stack

- **Platform**: Android
- **Language**: Kotlin / Java
- **Architecture**: MVVM with Clean Architecture
- **Networking**: Retrofit, OkHttp, WebSocket
- **UI**: Jetpack Compose / XML Layouts
- **Data**: Room, SharedPreferences
- **Security**: Encryption for sensitive data, secure storage

## Architecture

The app follows MVVM pattern with Clean Architecture principles:
- **Presentation Layer**: UI components, ViewModels
- **Domain Layer**: Use cases, business logic
- **Data Layer**: Repositories, API services, local database

## Key Achievements

- Implemented real-time market data updates via WebSocket
- Built secure wallet system with encryption
- Designed intuitive UI for complex trading operations
- Integrated multiple payment gateways for recharge functionality

## Timeline

- **Started**: 2022
- **Status**: Completed

## Screenshots

### App Interface

<p align="center">
  <img src="images/screenshot_02.jpg" width="200"/>
</p>

### Wallet & Assets

<table>
  <tr>
    <td align="center"><img src="images/main_wallet.jpg" width="200"/><br/><sub>Wallet dashboard with total assets</sub></td>
    <td align="center"><img src="images/main_wallet2.jpg" width="200"/><br/><sub>Wallet with earnings breakdown</sub></td>
    <td align="center"><img src="images/main_product.jpg" width="200"/><br/><sub>Product dashboard with asset details</sub></td>
  </tr>
</table>

### Investment System

<table>
  <tr>
    <td align="center"><img src="images/invest.jpg" width="200"/><br/><sub>Investment details form</sub></td>
    <td align="center"><img src="images/invest2.jpg" width="200"/><br/><sub>Investment flow with error/success states</sub></td>
    <td align="center"><img src="images/invest_detail.jpg" width="200"/><br/><sub>Investment detail screen (BTC, 7-day cycle)</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="images/main_invest_list.jpg" width="200"/><br/><sub>Invested list with daily earnings</sub></td>
    <td align="center"><img src="images/main_invested.jpg" width="200"/><br/><sub>Investment cards for BTC/ETH</sub></td>
  </tr>
</table>

### Account & Transactions

<table>
  <tr>
    <td align="center"><img src="images/account_info.jpg" width="200"/><br/><sub>Account info with crypto wallet addresses</sub></td>
    <td align="center"><img src="images/withdrawa.jpg" width="200"/><br/><sub>BTC withdrawal form</sub></td>
    <td align="center"><img src="images/trans.jpg" width="200"/><br/><sub>Transaction filter overlay</sub></td>
  </tr>
</table>

### VIP System

<table>
  <tr>
    <td align="center"><img src="images/vip_rule.jpg" width="200"/><br/><sub>VIP level progress and bonus tiers</sub></td>
  </tr>
</table>
