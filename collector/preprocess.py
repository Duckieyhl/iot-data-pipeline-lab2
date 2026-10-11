import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient

# Đọc dữ liệu từ InfluxDB ra Pandas DataFrame
def fetch_raw_data():
    client = InfluxDBClient(url="http://localhost:8086", token="YOUR_INFLUXDB_TOKEN", org="ptit")
    query = 'from(bucket:"iot_telemetry") |> range(start: -1h)'
    df = client.query_api().query_data_frame(query)
    return df

def clean_data(df):
    # 1. Phát hiện và xử lý Outlier bằng IQR (Interquartile Range)
    Q1 = df['temperature'].quantile(0.25)
    Q3 = df['temperature'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df['temperature_clean'] = np.where((df['temperature'] < lower_bound) | (df['temperature'] > upper_bound), np.nan, df['temperature'])
    
    # 2. Xử lý giá trị thiếu bằng phương pháp Nội suy (Interpolate)
    df['temperature_clean'] = df['temperature_clean'].interpolate(method='linear')
    
    # 3. Resampling theo cửa sổ 1 phút và tính Rolling Mean
    df_resampled = df.resample('1T', on='_time').mean()
    df_resampled['rolling_mean'] = df_resampled['temperature_clean'].rolling(window=3).mean()
    
    return df_resampled

if __name__ == "__main__":
    raw_df = fetch_raw_data()
    cleaned_df = clean_data(raw_df)
    print(cleaned_df.head())
