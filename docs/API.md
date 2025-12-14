# API仕様書

## ベースURL

```
http://localhost:8000/api
```

## 共通仕様

### リクエストヘッダー

```
Content-Type: application/json
```

### レスポンス形式

すべてのレスポンスはJSON形式で返されます。

## エンドポイント一覧

### 1. 急所マスターデータ

#### 1.1 全急所取得

```
GET /vital-points/
```

**レスポンス例**:
```json
[
  {
    "id": 1,
    "number": "①",
    "name": "百会",
    "reading": "ひゃくえ",
    "category": "頭部",
    "image_file": "Scan2025-12-13_140703_000.png"
  },
  ...
]
```

#### 1.2 急所詳細取得

```
GET /vital-points/{id}/
```

**パラメータ**:
- `id`: 急所ID

**レスポンス例**:
```json
{
  "id": 1,
  "number": "①",
  "name": "百会",
  "reading": "ひゃくえ",
  "category": "頭部",
  "image_file": "Scan2025-12-13_140703_000.png"
}
```

### 2. 学習履歴

#### 2.1 全学習履歴取得

```
GET /learning-history/
```

**レスポンス例**:
```json
[
  {
    "id": 1,
    "vital_point": {
      "id": 1,
      "number": "①",
      "name": "百会",
      "reading": "ひゃくえ",
      "category": "頭部",
      "image_file": "Scan2025-12-13_140703_000.png"
    },
    "correct_count": 5,
    "incorrect_count": 2,
    "last_learned_at": "2025-12-14T10:30:00Z",
    "accuracy_rate": 71.43
  },
  ...
]
```

#### 2.2 統計情報取得

```
GET /learning-history/statistics/
```

**レスポンス例**:
```json
{
  "total_correct": 150,
  "total_incorrect": 50,
  "total_attempts": 200,
  "accuracy_rate": 75.0
}
```

#### 2.3 苦手な急所取得

```
GET /learning-history/weak_points/
```

不正解が多い順に最大10件を返します。

**レスポンス例**:
```json
[
  {
    "id": 5,
    "vital_point": {
      "id": 15,
      "number": "⑤",
      "name": "太淵",
      "reading": "たいえん",
      "category": "上肢",
      "image_file": "Scan2025-12-13_140703_001.png"
    },
    "correct_count": 2,
    "incorrect_count": 8,
    "last_learned_at": "2025-12-14T09:15:00Z",
    "accuracy_rate": 20.0
  },
  ...
]
```

### 3. クイズセッション

#### 3.1 新規セッション開始

```
POST /quiz-sessions/start_new_session/
```

**リクエストボディ**:
```json
{
  "weak_points_mode": false
}
```

**パラメータ**:
- `weak_points_mode` (boolean, optional): 苦手な問題モードで開始するか
  - `true`: 不正解が多い順に出題
  - `false` (デフォルト): ランダム順に出題

**レスポンス例**:
```json
{
  "id": 1,
  "status": "active",
  "current_question_order": 1,
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:00:00Z"
}
```

#### 3.2 現在の問題取得

```
GET /quiz-sessions/{session_id}/current_question/
```

**パラメータ**:
- `session_id`: セッションID

**レスポンス例**:
```json
{
  "question_id": 1,
  "question_order": 1,
  "total_questions": 70,
  "number": "①",
  "category": "頭部",
  "image_file": "Scan2025-12-13_140703_000.png",
  "choices": [
    {
      "id": 1,
      "name": "百会",
      "reading": "ひゃくえ"
    },
    {
      "id": 5,
      "name": "天柱",
      "reading": "てんちゅう"
    },
    {
      "id": 12,
      "name": "完骨",
      "reading": "かんこつ"
    },
    {
      "id": 8,
      "name": "風池",
      "reading": "ふうち"
    }
  ]
}
```

**エラーレスポンス（全問回答済み）**:
```json
{
  "message": "全ての問題に回答済みです"
}
```

#### 3.3 回答送信

```
POST /quiz-sessions/{session_id}/submit_answer/
```

**パラメータ**:
- `session_id`: セッションID

**リクエストボディ**:
```json
{
  "question_id": 1,
  "answer_id": 1
}
```

**パラメータ説明**:
- `question_id`: SessionQuestionのID（current_questionレスポンスのquestion_id）
- `answer_id`: 選択した急所のID

**レスポンス例（正解）**:
```json
{
  "is_correct": true,
  "correct_answer": {
    "id": 1,
    "name": "百会",
    "reading": "ひゃくえ"
  },
  "message": "正解です！"
}
```

**レスポンス例（不正解）**:
```json
{
  "is_correct": false,
  "correct_answer": {
    "id": 1,
    "name": "百会",
    "reading": "ひゃくえ"
  },
  "message": "不正解です。正解は「百会（ひゃくえ）」です。"
}
```

#### 3.4 セッション一時停止

```
POST /quiz-sessions/{session_id}/pause/
```

**パラメータ**:
- `session_id`: セッションID

**レスポンス例**:
```json
{
  "id": 1,
  "status": "paused",
  "current_question_order": 15,
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:25:00Z"
}
```

#### 3.5 セッション再開

```
POST /quiz-sessions/{session_id}/resume/
```

**パラメータ**:
- `session_id`: セッションID

**レスポンス例**:
```json
{
  "id": 1,
  "status": "active",
  "current_question_order": 15,
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:30:00Z"
}
```

#### 3.6 セッション完了

```
POST /quiz-sessions/{session_id}/complete/
```

**パラメータ**:
- `session_id`: セッションID

セッションを完了状態にします。

**レスポンス例**:
```json
{
  "id": 1,
  "status": "completed",
  "current_question_order": 70,
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T11:00:00Z"
}
```

## エラーレスポンス

### 400 Bad Request

リクエストパラメータが不正な場合。

```json
{
  "error": "Invalid parameters",
  "detail": "answer_id is required"
}
```

### 404 Not Found

指定されたリソースが存在しない場合。

```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error

サーバー内部エラー。

```json
{
  "error": "Internal server error"
}
```

## フロントエンドAPIクライアント

### 使用例

```javascript
import { quizSessionAPI, learningHistoryAPI } from './api/client'

// セッション開始（通常モード）
const response = await quizSessionAPI.startNew(false)
const sessionId = response.data.id

// セッション開始（苦手な問題モード）
const response = await quizSessionAPI.startNew(true)

// 現在の問題取得
const question = await quizSessionAPI.getCurrentQuestion(sessionId)

// 回答送信
const result = await quizSessionAPI.submitAnswer(sessionId, {
  question_id: question.data.question_id,
  answer_id: selectedAnswerId
})

// 統計情報取得
const stats = await learningHistoryAPI.getStatistics()
```

## データフロー

### 学習セッションのフロー

```
1. POST /quiz-sessions/start_new_session/
   ↓ セッションID取得
2. GET /quiz-sessions/{id}/current_question/
   ↓ 問題データ取得
3. POST /quiz-sessions/{id}/submit_answer/
   ↓ 回答送信・学習履歴更新
4. 正解の場合 → 次の問題へ（ステップ2へ）
   不正解の場合 → 同じ問題を再出題（ステップ2へ）
5. 全問正解 → POST /quiz-sessions/{id}/complete/
```

### 学習履歴の更新タイミング

- 回答送信時（`submit_answer`）に自動的に更新
- 正解: `correct_count += 1`
- 不正解: `incorrect_count += 1`
- どちらの場合も `last_learned_at` を現在時刻で更新

## 注意事項

1. **セッションの有効期限**: 現在のところ有効期限はなく、セッションは永続的に保存される
2. **同時セッション**: 複数のセッションを同時に開始可能だが、フロントエンドでは1セッションずつ処理
3. **選択肢の重複**: 同じ名前の急所（例: 三里）は選択肢に重複して表示されない
4. **画像パス**: 画像はフロントエンドの静的ファイルとして配信されるため、APIレスポンスにはファイル名のみ含まれる
