document.getElementById('search-btn').onclick = async () => {
  const t = document.getElementById('ticker-input').value.trim();
  const res = await fetch(`/api/${t}`);
  const data = await res.json();
  if (res.status !== 200) {
    document.getElementById('result').innerText = data.error;
    return;
  }
  // ここで data.info と data.records をもとにHTML生成＆グラフ描画
  // 例：順位表示やChart.jsによる折れ線／棒グラフなど
};
