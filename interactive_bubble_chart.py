# 导入必要库
import pandas as pd
import os
import numpy as np
import plotly.express as px

# 设置当前工作路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("当前工作路径：", os.getcwd())

# 读取你的数据
df = pd.read_csv('./Data_Output/Results_with_outliers_flag.csv')

# 生成新指标和字段
df['diet_sex_group'] = df['diet_group'] + '_' + df['sex']
df['stability_score'] = np.sqrt(df['sd_watuse']**2 + df['sd_watscar']**2)

# 生成新的 color_group
def assign_color_group(row):
    if row['outliers'] == 1:
        return 'vegan_female_outlier'
    elif row['outliers'] == 2:
        return 'vegan_male_outlier'
    elif row['outliers'] == 3:
        return 'veggie_female_outlier'
    elif row['outliers'] == 4:
        return 'veggie_male_outlier'
    else:
        return row['diet_sex_group']

df['color_group'] = df.apply(assign_color_group, axis=1)

# 定义颜色映射
color_map = {
    'vegan_female': '#AEC6CF',          # 浅蓝色
    'vegan_male': '#D1C4E9',            # 薰衣草紫
    'veggie_female': '#A8E6CF',         # 薄荷绿
    'veggie_male': '#FFD3B6',           # 奶油黄
    'vegan_female_outlier': 'red',      # 离群统一红色
    'vegan_male_outlier': 'red',
    'veggie_female_outlier': 'red',
    'veggie_male_outlier': 'red'
}

# 自定义 color_group 的顺序
order = [
    'vegan_female',
    'vegan_male',
    'veggie_female',
    'veggie_male',
    'vegan_female_outlier',
    'vegan_male_outlier',
    'veggie_female_outlier',
    'veggie_male_outlier'
]

# 设置 color_group 为有序分类变量
df['color_group'] = pd.Categorical(df['color_group'], categories=order, ordered=True)


# 绘制交互式气泡图
fig = px.scatter(
    df,
    x='mean_watuse',       
    y='mean_watscar',       
    color='color_group',    # 关键：用新的 color_group
    color_discrete_map=color_map,
    size='stability_score',
    animation_frame='age_group',
    size_max=60,
    hover_name='grouping',
    hover_data={
        'mean_watuse': ':.2f',
        'mean_watscar': ':.2f',
        'outliers': True
    },
    category_orders={'color_group': order} 
)

# 自定义气泡样式（透明度+白色边框）
fig.update_traces(
    marker=dict(
        opacity=0.7,
        line=dict(color='white', width=1)
    )
)

# 微调整体布局
fig.update_layout(
    title={
        'text': (
            "Interactive Bubble Chart: Water Use vs Water Scarcity by Diet Group and Age<br>"
            "<span style='font-size:16px; color:gray;'>Analyzing Water Use Outliers and Scarcity Risks Among Vegan and Vegetarian Dietary Groups</span>"
        ),
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    title_font=dict(
        size=28,
        family='Arial',
        color='black'
    ),
    sliders=[{
        'active': 0,
        'currentvalue': {
            'prefix': 'Age Group: ',
            'font': {'size': 14, 'color': 'grey'},  # 当前值字体更小更淡
            'offset': 10  # 字和slider拉开一点
        },
        'pad': {'t': 10},   # 上下padding小一点
        'len': 0.8,         # 整个slider长度短一点
        'x': 0.1,           # 居中显示
        'y': -0.15,         # 位置更下方
        'font': {'size': 14},
        'steps': [],        # 必须保留，不然出错
    }],
    transition={'duration': 300},  # 平滑过渡
    sliderdefaults=dict(
        bgcolor='lightgrey',  # 背景色
        activebgcolor='deepskyblue',  # 选中后颜色
        bordercolor='lightgrey',
        borderwidth=1
    ),
    legend_title_text='Diet + Sex Group',
    legend=dict(
        title_font=dict(size=20, family='Arial'),
        font=dict(size=16, family='Arial'),
        bgcolor='rgba(255,255,255,0.6)',  # 更白更轻
        bordercolor='lightgrey',
        borderwidth=1,
        orientation='v',  # 纵向
        yanchor='top',
        y=0.8,
        xanchor='left',
        x=1.02  # 稍微靠外
    ),
    xaxis_title='Mean Water Use (liters/day)',
    xaxis=dict(
        range=[df['mean_watuse'].min()*0.8, df['mean_watuse'].max()*1.2],
        showline=True,
        linecolor='black',
        linewidth=2
    ),
    yaxis_title='Mean Water Scarcity (index)',
    yaxis=dict(
        range=[df['mean_watscar'].min()*0.8, df['mean_watscar'].max()*1.2],
        showline=True,
        linecolor='black',
        linewidth=2
    ),
    plot_bgcolor='white',
    autosize=True,
    margin=dict(l=50, r=50, t=100, b=50) # 留白，避免太挤
)

# 导出为HTML文件（可以浏览器打开看）
fig.write_html('./Data_Output/interactive_bubble_chart_final.html', full_html=True, include_plotlyjs='cdn', config={'responsive': True})


