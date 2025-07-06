from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
# 起動時に CSV を読み込んでおく
df_aci = pd.read_csv('ticker_aci.csv', dtype={'ticker': str})
df_data = pd.read_csv('merged_scores.csv', dtype={'code': str})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<ticker>')
def api_ticker(ticker):
    # ACIランキング
    total = len(df_aci)
    row = df_aci[df_aci['ticker']==ticker]
    if row.empty:
        return jsonify({'error':'該当ティッカーなし'}), 404

    # 各モードごとのランクを求める関数
    def get_rank(col):
        rank = int((df_aci[col] > row[col].iloc[0]).sum()) + 1
        return {'rank': rank, 'total': total}

    info = {'ticker': ticker}
    for col in ['revenue_aci_weighted','op_profit_aci_weighted','net_profit_aci_weighted','aci_weighted']:
        info[col] = {
            'value': float(row[col]),
            **get_rank(col)
        }
    # 予測 vs 実績の数値一覧
    recs = df_data[df_data['code']==ticker].to_dict(orient='records')
    return jsonify(info=info, records=recs)

if __name__=='__main__':
    app.run(debug=True)
