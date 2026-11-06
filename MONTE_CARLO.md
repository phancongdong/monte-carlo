# Mô phỏng Monte Carlo (Monte Carlo Simulation)

## 1. Khái niệm cốt lõi
**Mô phỏng Monte Carlo** là một kỹ thuật toán học tính toán xác suất bằng thuật toán **lấy mẫu ngẫu nhiên lặp lại hàng nghìn đến hàng triệu lần** để mô hình hóa hành vi và kết quả của các hệ thống phức tạp, phi tuyến tính và có độ bất định cao mà không thể giải bằng công thức giải tích đóng.

---

## 2. Nguyên lý hoạt động
1. **Mô hình hóa biến số đầu vào**: Gán các phân phối xác suất thực tế (Normal, Student-t, Log-normal, Empirical) cho các biến số thị trường hoặc thông số chiến lược.
2. **Sinh kịch bản ngẫu nhiên**: Dùng bộ tạo số ngẫu nhiên mô phỏng hàng ngàn chuỗi diễn biến giá hoặc trình tự lệnh độc lập.
3. **Phân tích thống kê đầu ra**: Tổng hợp kết quả từ toàn bộ các kịch bản để xây dựng phân phối xác suất, tính toán kỳ vọng (Expected Value), độ lệch chuẩn và khoảng tin cậy (Confidence Interval, ví dụ 95% CI).

---

## 3. Ứng dụng trong Tài chính & Quantitative Trading

### A. Kiểm định độ bền chiến lược (Robustness Stress-Testing)
- **Trade Shuffling & Bootstrap**: Hoán vị hoặc lấy mẫu có lặp lại thứ tự các giao dịch để kiểm tra xem hiệu suất quá khứ là do **năng lực thực tế (skill)** hay do **may mắn thời điểm (luck)**.
- **Phân phối sụt giảm vốn (Drawdown Analysis)**: Dự phóng mức sụt giảm tài khoản sâu nhất (Max Drawdown ở phân vị 95% hoặc 99%) và đo lường xác suất cháy tài khoản (*Risk of Ruin*).

### B. Tái lấy mẫu dữ liệu giá nến (Market Resampling)
- **Moving Block Bootstrap**: Tái lấy mẫu các khối nến OHLCV để tạo ra các kịch bản thị trường mới mà vẫn bảo toàn tính tự tương quan chuỗi thời gian (autocorrelation) và biến động cụm (volatility clustering).
- **Gaussian Noise Injection**: Bổ sung nhiễu ngẫu nhiên vào dữ liệu giá để kiểm tra độ nhạy và tính vững chắc của tín hiệu vào/ra lệnh.

### C. Quản trị rủi ro danh mục (Portfolio Risk)
- Ước lượng **Value at Risk (VaR)** và **Conditional VaR (CVaR)** ở các ngưỡng tin cậy cao, ứng phó với hiện tượng phân phối đuôi nặng (*fat-tail risk*) và sự kiện thiên nga đen.

---

## 4. Cách sử dụng trong Framework

```python
from jesse.research.monte_carlo import monte_carlo_trades, monte_carlo_candles

# Mô phỏng hoán vị chuỗi lệnh (Trade-order Monte Carlo)
trade_results = monte_carlo_trades(trades=my_trades, num_scenarios=1000)
print("Median Drawdown:", trade_results["max_drawdown_median"])
print("95th Percentile Drawdown:", trade_results["max_drawdown_95th"])

# Mô phỏng nến thị trường (Candles-based Monte Carlo)
candle_results = monte_carlo_candles(candles=my_candles, num_scenarios=500, pipeline_type="moving_block")
```
