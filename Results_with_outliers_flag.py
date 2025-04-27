import pandas as pd
import os

# 设置当前工作路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("当前工作路径：", os.getcwd())

# 读取数据
df = pd.read_csv("./Results_21Mar2022.csv")

# 保留需要的列
columns_needed = [
    'mc_run_id', 'grouping', 'mean_watscar', 'mean_watuse', 'sd_watscar', 'sd_watuse',
    'n_participants', 'sex', 'diet_group', 'age_group'
]
df = df[columns_needed]

df = df[df['diet_group'].isin(['vegan', 'veggie'])].copy()

# 生成 diet_sex_group
df['diet_sex_group'] = df['diet_group'] + '_' + df['sex']

# 定义对应关系
diet_sex_to_outlier_code = {
    'vegan_female': 1,
    'vegan_male': 2,
    'veggie_female': 3,
    'veggie_male': 4
}

# 初始化 outliers=0（默认都不是离群）
df['outliers'] = 0

# 对每个 grouping 分组处理
for group_name, group_data in df.groupby('grouping'):
    if group_data.empty:
        continue

    # 计算四分位数
    q1 = group_data['mean_watuse'].quantile(0.25)
    q3 = group_data['mean_watuse'].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # 找到离群值
    outlier_indices = group_data[
        (group_data['mean_watuse'] < lower_bound) | (group_data['mean_watuse'] > upper_bound)
    ].index

    # 给离群点赋对应的编码
    for idx in outlier_indices:
        diet_sex = df.at[idx, 'diet_sex_group']
        code = diet_sex_to_outlier_code.get(diet_sex, 0)
        df.at[idx, 'outliers'] = code

# 保存新表
df.to_csv("./Data_Output/Results_with_outliers_flag.csv", index=False)

