# GitHubへのアップロード手順

このドキュメントでは、プロジェクトをGitHubにアップロードする手順を説明します。

## 前提条件

- GitHubアカウントを持っている
- Gitがインストールされている
- プロジェクトがローカルでGit管理されている（完了済み）

## 手順

### ステップ1: GitHubで新しいリポジトリを作成

1. **GitHubにログイン**
   - https://github.com にアクセス
   - アカウントにログイン

2. **新規リポジトリを作成**
   - 右上の「+」アイコンをクリック
   - 「New repository」を選択

3. **リポジトリ情報を入力**
   - **Repository name**: `vital_points` または `vital-points-learning-app`
   - **Description**: `人体の急所70箇所を学習するWebアプリケーション`
   - **Public/Private**: お好みで選択
     - Public: 誰でも閲覧可能
     - Private: 自分と招待した人のみ閲覧可能
   - **Initialize this repository with**:
     - ❌ README（既にあるのでチェックしない）
     - ❌ .gitignore（既にあるのでチェックしない）
     - ❌ license（後で追加可能）

4. **「Create repository」をクリック**

### ステップ2: ローカルリポジトリとGitHubを接続

GitHubでリポジトリを作成すると、接続用のURLが表示されます。以下のコマンドを実行:

#### HTTPSを使用する場合（推奨）

```bash
# プロジェクトディレクトリに移動
cd /home/administrator/Projects/vital_points

# リモートリポジトリを追加
git remote add origin https://github.com/YOUR_USERNAME/vital_points.git

# リモートリポジトリを確認
git remote -v
```

`YOUR_USERNAME`は自分のGitHubユーザー名に置き換えてください。

#### SSHを使用する場合（SSH鍵設定済みの場合）

```bash
git remote add origin git@github.com:YOUR_USERNAME/vital_points.git
```

### ステップ3: コードをGitHubにプッシュ

```bash
# メインブランチの名前を確認（mainまたはmaster）
git branch

# GitHubにプッシュ
git push -u origin main
```

初回プッシュ時、認証情報の入力を求められる場合があります:
- **HTTPS**: GitHubのユーザー名とパスワード（またはPersonal Access Token）
- **SSH**: SSH鍵のパスフレーズ（設定している場合）

### ステップ4: 認証設定（必要な場合）

#### Personal Access Token（PAT）を使用（推奨）

GitHubはパスワード認証を廃止したため、Personal Access Tokenを使用します。

1. **GitHubでトークンを作成**
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 「Generate new token (classic)」をクリック
   - Note: `vital_points_upload`
   - Expiration: お好みの期間を選択
   - Scopes:
     - ✅ repo（全てのリポジトリアクセス）
   - 「Generate token」をクリック
   - **トークンをコピー**（この画面を離れると二度と表示されません）

2. **プッシュ時にトークンを使用**
   ```bash
   git push -u origin main
   ```
   - Username: GitHubユーザー名
   - Password: コピーしたトークン（パスワードではない）

#### 認証情報のキャッシュ（オプション）

毎回入力するのを避けるため、認証情報をキャッシュできます:

```bash
# 15分間キャッシュ
git config --global credential.helper cache

# 1時間キャッシュ
git config --global credential.helper 'cache --timeout=3600'

# 永続的に保存（Linux）
git config --global credential.helper store
```

## プッシュ後の確認

1. GitHubのリポジトリページにアクセス
2. ファイルがアップロードされているか確認
3. README.mdが正しく表示されているか確認

## 今後の更新手順

プロジェクトを更新した後、GitHubに反映する手順:

```bash
# 変更をステージング
git add .

# コミット
git commit -m "更新内容の説明"

# GitHubにプッシュ
git push
```

## トラブルシューティング

### エラー: "remote origin already exists"

既にリモートが設定されている場合:

```bash
# 既存のリモートを削除
git remote remove origin

# 新しいリモートを追加
git remote add origin https://github.com/YOUR_USERNAME/vital_points.git
```

### エラー: "failed to push some refs"

リモートに新しい変更がある場合:

```bash
# リモートの変更を取得してマージ
git pull origin main --rebase

# 再度プッシュ
git push -u origin main
```

### エラー: "Permission denied (publickey)"

SSH鍵が設定されていない場合:
- HTTPSを使用するか
- SSH鍵を設定（https://docs.github.com/ja/authentication/connecting-to-github-with-ssh）

## セキュリティに関する注意

### 機密情報の確認

プッシュ前に以下を確認してください:

✅ `.gitignore`が正しく設定されている
✅ データベースファイル（`db.sqlite3`）が除外されている
✅ 環境変数ファイル（`.env`）が除外されている
✅ 仮想環境（`venv/`）が除外されている
✅ ログファイルが除外されている

現在の`.gitignore`は適切に設定済みです。

### 公開リポジトリの場合

Public リポジトリにする場合:
- APIキーや秘密鍵は含めない
- 本番環境の設定情報は含めない
- データベースは空の状態でOK（マイグレーションファイルのみ含める）

## リポジトリの説明を追加

GitHubリポジトリページで「About」セクションを編集し、以下を追加することを推奨:

- **Description**: 人体の急所70箇所を学習するWebアプリケーション
- **Website**: デプロイした場合のURL
- **Topics**:
  - `react`
  - `django`
  - `education`
  - `learning-app`
  - `quiz`
  - `japanese`

## まとめ

基本的な流れ:

1. GitHubでリポジトリ作成
2. `git remote add origin <URL>`
3. `git push -u origin main`
4. 認証情報を入力
5. GitHubで確認

これでプロジェクトがGitHubにアップロードされます。
