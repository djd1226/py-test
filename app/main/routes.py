import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import render_template, request, redirect, url_for, current_app
from app.main import bp
from app.main.forms import EntryForm

# 加载数据函数，从 JSON 文件读取数据并返回 DataFrame
def load_data():
    data_file = current_app.config['DATA_FILE']
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as file:
                data = json.load(file)
            if data:
                return pd.DataFrame(data)
            else:
                return pd.DataFrame(columns=[])
        except json.JSONDecodeError:
            return pd.DataFrame(columns=[])
    else:
        return pd.DataFrame(columns=[])

# 保存数据函数，将 DataFrame 写入 JSON 文件
def save_data(df):
    data_file = current_app.config['DATA_FILE']
    with open(data_file, 'w') as file:
        json.dump(df.to_dict(orient='records'), file)

# 主页路由，渲染 index.html
@bp.route('/')
def index():
    return render_template('index.html')

# 显示数据表的路由，渲染 table.html 并传递数据
@bp.route('/table')
def table():
    df = load_data()
    return render_template('table.html', data=df.to_html(classes='table table-striped'))


# 路由：显示图表页面
@bp.route('/charts')
def charts():
    df = load_data()
    if df.empty:
        return "没有数据可显示"
    
    fig, ax = plt.subplots()
    df.plot(kind='bar', x='日期', y='销售额', ax=ax)
    ax.set_title('销售数据')
    ax.set_xlabel('日期')
    ax.set_ylabel('销售额')
    # 保存图表到文件
    chart_path = os.path.join('app', 'static', 'charts', 'sales_chart.png')
    plt.savefig(chart_path)

    # 关闭图表
    plt.close(fig)

    # 渲染模板，传递图表路径
    chart_url = url_for('static', filename='charts/sales_chart.png')
    return render_template('charts.html', chart_url=chart_url)

# 路由：添加数据页面
@bp.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    form = EntryForm()
    if form.validate_on_submit():
        date = form.date.data.strftime('%Y-%m-%d')
        sales = float(form.sales.data)
        df = load_data()
        new_entry = {'日期': date, '销售额': sales}
        df = pd.concat([df,pd.DataFrame([new_entry])],ignore_index=True)
        save_data(df)
        return redirect(url_for('main.table'))
    return render_template('add_entry.html', form=form)

