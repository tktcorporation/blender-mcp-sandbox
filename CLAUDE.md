# Blender MCP Sandbox

## 画像から3Dモデル作成の一般的手法

### 画像解析フェーズ
1. **構成要素の分析**
   - 基本形状の特定（円柱、球、立方体など）
   - パーツ間の関係性・接続方法
   - 色・マテリアル情報の抽出

2. **構造化データへの変換**
   - 各パーツの寸法比率
   - 座標・回転・スケール情報
   - 階層構造の定義

### モデリング手法

#### 1. 画像解析→構造化データ→モデリング
- **基本形状の特定**：プリミティブ（円柱、球、立方体等）への分解
- **寸法比率の計算**：相対的なサイズ関係の数値化
- **色・マテリアル情報**：RGB値、材質特性の抽出

#### 2. プリミティブ分解→組み立てアプローチ
- 基本形状での近似
- ブーリアン演算による組み合わせ
- 段階的な詳細追加

#### 3. ハイブリッドアプローチ
- AI生成（Hyper3D等）で大まかな形状作成
- 画像解析データで詳細調整
- プロシージャルモデリングで補完

### 実装パターン

#### A. 段階的構築
1. プリミティブ配置
2. 形状調整・変形
3. マテリアル適用
4. 詳細追加・最適化

#### B. データ駆動型
- JSON等で構造定義
- パラメータ化された生成関数
- 再利用可能なコンポーネント設計

### Blender MCP での実装方針
- `mcp__blender__execute_blender_code` を使用してPythonでプロシージャル生成
- 各パーツを段階的に作成・組み合わせ
- パラメータ化による調整の容易性確保

## 実装環境

### 開発環境
- **Python**: 3.11+
- **パッケージ管理**: uv
- **コード品質**: ruff (linting & formatting)
- **型チェック**: mypy

### ユーティリティライブラリ
`image_to_3d_utils.py` に実装済み：

#### ImageTo3DModeler
基本的なモデリング操作クラス
- `create_primitive()`: プリミティブ（円柱、立方体、球、円錐）の作成
- `create_material()`: マテリアル作成とノード設定
- `apply_material()`: オブジェクトへのマテリアル適用
- `boolean_operation()`: ブーリアン演算による形状結合

#### ParametricModeler  
データ駆動型モデル生成クラス
- `create_from_json()`: JSON定義からの自動モデル生成
- パラメータ化されたワークフロー

#### ShapeAnalyzer
形状・色彩解析ユーティリティ
- `analyze_proportions()`: 画像比率分析
- `color_to_blender()`: 16進数→Blender RGBA変換

### 使用方法
```python
# Blender内でライブラリをインポート
exec(open('image_to_3d_utils.py').read())

# 基本的な使用例
modeler = ImageTo3DModeler()
obj = modeler.create_primitive('cylinder', 'torch_handle', (0,0,0), (0.2,0.2,2))
```

### 開発コマンド
```bash
# コード品質チェック
uv run --group dev ruff check image_to_3d_utils.py

# 自動修正
uv run --group dev ruff check --fix image_to_3d_utils.py

# 型チェック  
uv run --group dev mypy image_to_3d_utils.py
```