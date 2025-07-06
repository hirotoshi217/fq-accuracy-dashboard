## 🐍 app.py
from flask import Flask, render_template, request, abort
import pandas as pd
import os

app = Flask(__name__)

data_dir = os.path.join(os.path.dirname(__file__), 'data')
df_aci = pd.read_csv(os.path.join(data_dir, 'ticker_aci.csv'), dtype={'ticker': str})
df_scores = pd.read_csv(os.path.join(data_dir, 'merged_scores.csv'), dtype={'code': str})

def compute_rank(series, code):
    # 順位：1 が最高
    sorted_vals = series.sort_values(ascending=False).reset_index()
    sorted_vals['rank'] = sorted_vals.index + 1
    s = sorted_vals.set_index(series.name)
    val = df_aci.loc[df_aci['ticker']==code, series.name].iloc[0]
    total = len(series)
    rank = int(sorted_vals[sorted_vals[series.name]==val]['rank'])
    return rank, total

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        if code == '':
            abort(400, 'Ticker code is required')
        # ACI metrics
        try:
            row = df_aci[df_aci['ticker'] == code].iloc[0]
        except IndexError:
            abort(404, f'{code} not found')

        # 各指標ランキング
        ranks = {}
        for m in ['revenue_aci_weighted', 'op_profit_aci_weighted', 'net_profit_aci_weighted', 'aci_weighted']:
            r, total = compute_rank(df_aci[m], code)
            ranks[m] = {'rank': r, 'total': total, 'value': row[m]}

        # 時系列データ (予想vs実績)
        df_t = df_scores[df_scores['code']==code].sort_values('period')
        plot_data = {
            'periods': df_t['period'].tolist(),
            'pred': {
                'revenue': df_t['revenue'].tolist(),
                'op_profit': df_t['op_profit'].tolist(),
                'net_profit': df_t['net_profit'].tolist()
            },
            'actual': {
                'revenue': df_t['actual_revenue'].tolist(),
                'op_profit': df_t['actual_op_profit'].tolist(),
                'net_profit': df_t['actual_net_profit'].tolist()
            }
        }
        result = {'code': code, 'ranks': ranks, 'plot_data': plot_data}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)