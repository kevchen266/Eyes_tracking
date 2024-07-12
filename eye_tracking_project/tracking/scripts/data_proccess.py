import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = "/Users/kev19/Desktop/Project/summer project/eyestracking/backend/eye_tracking_project/videos/testing.csv"  # 请将这里替换为你的输入文件路径
df = pd.read_csv(file_path)

# 显示前几行数据
print("原始数据：")
print(df.head())

# 识别并处理异常值
def remove_outliers(df, threshold=3):
    z_scores = (df - df.mean()) / df.std()
    df_clean = df[(np.abs(z_scores) < threshold).all(axis=1)]
    return df_clean

# 对数值列应用去除异常值的方法
numeric_columns = df.select_dtypes(include=[np.number]).columns
df_clean = df.copy()

print("\n数值列：", numeric_columns)

df_clean[numeric_columns] = remove_outliers(df[numeric_columns])

print("\n去除异常值后的数据：")
print(df_clean[numeric_columns].head())

# 填充缺失值
for column in numeric_columns:
    df_clean[column].fillna(df_clean[column].median(), inplace=True)

# 保存清理后的数据
output_file_path = "/Users/kev19/Desktop/Project/summer project/eyestracking/backend/eye_tracking_project/videos/cleaned_testing.csv"  # 请将这里替换为你的输出文件路径
df_clean.to_csv(output_file_path, index=False)

# 打印清理后的数据统计信息
print("\n清理后的数据统计信息：")
print(df_clean.describe())

# 生成清理后数据的可视化图
plt.figure(figsize=(10, 6))

# 绘制瞳孔位置
plt.scatter(df_clean['pupil_x'], df_clean['pupil_y'], color='blue', label='瞳孔位置')

# 绘制眼睛位置
plt.scatter(df_clean['eye_x'], df_clean['eye_y'], color='red', label='眼睛位置')

plt.xlabel('X 坐标')
plt.ylabel('Y 坐标')
plt.legend()
plt.title('清理后眼睛和瞳孔位置')
plt.grid(True)
plt.show()

# 计算瞳孔和眼睛位置的差异
df_clean['diff_x'] = df_clean['pupil_x'] - df_clean['eye_x']
df_clean['diff_y'] = df_clean['pupil_y'] - df_clean['eye_y']

# 检查差异的统计信息
diff_stats_info = df_clean[['diff_x', 'diff_y']].describe()

# 打印差异统计信息
print("\n差异统计信息：")
print(diff_stats_info)
