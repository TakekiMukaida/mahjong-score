import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

UMA = [30, 10, -10, -30] # 1位50点、2位10点、3位-10点、4位-30点
OKA = [25000, 30000] # 25000点持ち30000点返し

# Mリーグルールに基づくポイント計算
def calculate_points(scores):
    # スコアの合計が1000点か確認
    sum_scores = sum([int(score) for score in scores])
    if sum_scores != 1000:
        print("ERROR! - sum is wrong. sum = " + str(sum_scores))

    # ボーナス点
    bonus = UMA.copy()
    bonus[0] += 4 * (OKA[1] - OKA[0]) * 0.001
    
    # 素点に基づいて順位を決定
    sorted_scores = sorted(scores, reverse = True)
    ranks = [sorted_scores.index(score) for score in scores]

    for i, score in enumerate(scores):
        scores[i] = int(score) * 100 - OKA[1]
    
    # ポイント計算
    points = [round((score / 1000 + bonus[rank]) * 10) / 10 for score, rank in zip(scores, ranks)]

    #print(points)

    return points

# CSVファイルの読み込みと処理
def process_file(file_path):
    # ファイル読み込み
    df = pd.read_csv(file_path)
    
    # スコア列を取得
    players = df.columns.tolist()
    all_points = [[0,0,0,0]]
    
    # 各試合のポイントを計算
    for _, row in df.iterrows():
        scores = row[players].values
        points = calculate_points(scores)
        all_points.append(points)

    # ポイント変化の累積計算
    cumulative_points = pd.DataFrame(all_points, columns=[f'player{i}' for i in range(1, 5)]).cumsum()

    # グラフ化
    plot_points(players, cumulative_points)

    # 累積ポイントを保存
    output_file = 'cumulative_points.csv'
    cumulative_points.to_csv(output_file, index=False)

# グラフ描画
players = ["Player1", "Player2", "Player3", "Player4"]

def plot_points(players, cumulative_points):
    plt.figure(figsize=(10, 6))
    for i, player in enumerate(cumulative_points.columns):
        plt.plot(
            cumulative_points.index, 
            cumulative_points[player], 
            label = players[i]
        )
    
    plt.xlabel("number of matches")
    plt.ylabel("points")
    
    plt.xlim(0, len(cumulative_points) - 1)
    
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer = True))
    plt.savefig("points_change_graph.png")

# メイン処理
if __name__ == "__main__":
    input_file = "scores.csv"
    process_file(input_file)
