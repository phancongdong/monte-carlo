# Monte Carlo Simulation & Quantitative Trading Framework

An advanced algorithmic trading and quantitative research framework in Python, specializing in strategy robustness verification, risk modeling, and Monte Carlo simulation.

---

## 🎲 Tổng quan về Mô phỏng Monte Carlo (Monte Carlo Simulation)

**Mô phỏng Monte Carlo** là một kỹ thuật toán học sử dụng thuật toán **lấy mẫu ngẫu nhiên lặp lại hàng nghìn đến hàng triệu lần** để mô hình hóa phân phối xác suất của các kết quả trong những hệ thống tài chính phức tạp, có độ bất định cao mà không thể giải bằng công thức giải tích đóng.

### Vai trò cốt lõi trong Quantitative Trading:
1. **Kiểm định độ bền chiến lược (Robustness Stress-testing)**:
   - **Trade-Order Shuffling & Bootstrap**: Hoán vị và tái lấy mẫu thứ tự các lệnh đã khớp để kiểm tra độ nhạy đối với thời điểm vào lệnh, tách biệt rõ ràng giữa **năng lực thực tế (skill)** và **may mắn ngẫu nhiên (luck)**.
   - **Phân phối sụt giảm vốn (Drawdown Distribution)**: Dự phóng mức sụt giảm tài khoản lớn nhất (Max Drawdown ở phân vị 95% hoặc 99%) và xác định xác suất cháy tài khoản (*Risk of Ruin*).
2. **Mô phỏng dữ liệu thị trường (Market Resampling)**:
   - **Moving Block Bootstrap**: Tái lấy mẫu các khối nến OHLCV nhằm kiểm tra chiến lược trên nhiều chế độ thị trường mới nhưng vẫn bảo toàn cấu trúc tự tương quan (autocorrelation) và biến động cụm (volatility clustering).
   - **Gaussian Noise Injection**: Bổ sung nhiễu có kiểm soát vào chuỗi giá để kiểm tra độ ổn định của các ngưỡng kích hoạt tín hiệu.
3. **Quản trị rủi ro danh mục (Risk Management)**:
   - Ước lượng **Value at Risk (VaR)** và **Conditional VaR (CVaR)** ở các khoảng tin cậy cao, ứng phó với rủi ro thiên nga đen và phân phối đuôi nặng (*fat-tail risk*).

---

## Core Capabilities

### 1. Monte Carlo Robustness Analysis
- **Trade-Order Shuffling**: Stress-test execution paths by permuting historical trade sequences to detect sequence-of-returns risk and probability of ruin.
- **Moving Block Bootstrap**: Resample candle blocks to evaluate strategy stability against market regime changes while preserving autocorrelation.
- **Gaussian Noise Injection**: Perturb OHLCV series with controlled noise to test signal sensitivity.
- **Confidence Intervals & Drawdown Distributions**: Calculate 95% confidence intervals for Sharpe ratio, Sortino, and maximum drawdown percentiles.

### 2. Systematic Backtesting Engine
- Multi-timeframe and multi-asset concurrent backtesting.
- Fast execution with zero look-ahead bias.
- Accurate slippage, fee modeling, and position sizing.
- Comprehensive metrics: Sharpe, Sortino, Calmar, Win Rate, Expectancy, Omega, Tail Ratio.

### 3. Strategy Optimization
- Integrated hyperparameter search powered by Optuna.
- Multi-core and cluster parallelization via Ray.
- Overfitting detection and parameter stability validation.

### 4. Machine Learning & Research Pipeline
- Labelled training dataset generation directly from backtest signals.
- Support for scikit-learn classifiers and regressors.
- Full research API for interactive exploration in Jupyter Notebooks.

---

## Quick Start

### Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### Run Monte Carlo Simulation
```python
from montecarlo.research.monte_carlo import monte_carlo_trades, monte_carlo_candles

# 1. Run trade-order permutation simulation
results = monte_carlo_trades(trades=trade_history, num_scenarios=1000)
print(f"Median Max Drawdown: {results['max_drawdown_median']:.2f}%")
print(f"95th Percentile Max Drawdown: {results['max_drawdown_95th']:.2f}%")

# 2. Run candle-based moving block bootstrap simulation
candle_sim = monte_carlo_candles(candles=candles, num_scenarios=500, pipeline_type="moving_block")
```

---

## Disclaimer
This software is provided for research and educational purposes only. Always thoroughly validate any quantitative model before real capital deployment.
