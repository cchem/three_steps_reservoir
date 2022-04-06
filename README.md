# three_steps_reservoir

三段水槽のシミュレーションを行うために作成したリポジトリです。  
横河電機のプロセスAIのプレスリリース中で、三段水槽の水量管理はマニュアル制御は容易ではないと書かれていたため、実際どの程度難しいのか検証するために作成しました。

## 実行方法
```
python src/machine.py
```

# 感想
プレスリリースの通り、見た目から想像されるよりはだいぶ難しく感じた。  
ただし、一度コツをつかめば方針が掴めるため、ゲームとしてはそれほど難しくはない。  
一方、複数のパラメータを同時に操作し最速で水位を合わせるのは非常に難しいと思った。

## Todo
- 目標値を表示する機能の実装
- 一時停止 or 再生ボタンの実装
- 目標値を達成したかを判定してゲーム風味にする機能の実装
- 水位の変化をアニメーションとして表示する機能の実装？  
既にプログラムが重いので動作しなくなる可能性あり。
- 水槽同士を繋ぐパイプの実装  
(バルブを開くとすぐに次の水槽に送られるようだと制御が簡単な可能性があるため)
- メインの水槽が空になった時の例外処理  


## 参考
[https://www.yokogawa.co.jp/library/videos/product-overviews/ai-control-3-levels/](https://www.yokogawa.co.jp/library/videos/product-overviews/ai-control-3-levels/)
