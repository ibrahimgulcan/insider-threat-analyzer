from flask import Flask, render_template, request
import pandas as pd
import math

app = Flask(__name__)

df_main = pd.read_csv('data/final_risk_table.csv')

@app.route('/')
def index():
    min_puan = int(request.args.get('min_puan', 0))
    max_puan = int(request.args.get('max_puan', 100))

    filtrelenmis_df = df_main[
        (df_main['ultimate_risk_skoru'] >= min_puan) & 
        (df_main['ultimate_risk_skoru'] <= max_puan)
    ]

    istatistikler = {
        'toplam_kisi': len(filtrelenmis_df),
        'kirmizi_alarm': len(filtrelenmis_df[filtrelenmis_df['ultimate_risk_skoru'] >= 80]),
        'ortalama_risk': round(filtrelenmis_df['ultimate_risk_skoru'].mean(), 1) if not filtrelenmis_df.empty else 0
    }

    tum_liste = filtrelenmis_df.sort_values(by='ultimate_risk_skoru', ascending=False).to_dict(orient='records')
    
    return render_template('index.html', users=tum_liste, min_puan=min_puan, max_puan=max_puan, stats=istatistikler)

@app.route('/kullanici/<kullanici_id>')
def detay(kullanici_id):
    kullanici_bilgisi = df_main[df_main['user'] == kullanici_id]
    
    if not kullanici_bilgisi.empty:
        user_data = kullanici_bilgisi.iloc[0].to_dict()
        return render_template('detay.html', user=user_data)
    else:
        return "Kullanıcı bulunamadı!", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)