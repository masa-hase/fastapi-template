# API DTOs (Data Transfer Objects)

このディレクトリには、プレゼンテーション層のDTOが含まれます。

## 構造

各ドメインごとにファイルを作成し、関連するリクエスト/レスポンスDTOをまとめます：

```
dtos/
├── greeting_dtos.py    # Greeting関連のリクエスト/レスポンス
├── user_dtos.py        # User関連のリクエスト/レスポンス（例）
└── order_dtos.py       # Order関連のリクエスト/レスポンス（例）
```

## 命名規則

- **リクエストDTO**: `{Feature}Request` (例: `PersonalizedGreetingRequest`)
- **レスポンスDTO**: `{Feature}Response` (例: `GreetingResponse`)
- **共通DTO**: `{Feature}DTO` (例: `PaginationDTO`)

## DDD原則

1. **DTOはプレゼンテーション層に属する**: ドメインモデルとは独立
2. **検証はDTOレベルで実施**: 基本的な入力検証
3. **ビジネスロジックは含まない**: 単純なデータ構造のみ
4. **ドメインモデルとの変換**: ユースケース層で実施

## 例

```python
# greeting_dtos.py
class PersonalizedGreetingRequest(BaseModel):
    """リクエストDTO: 基本的な検証のみ"""
    name: str = Field(..., min_length=1, max_length=100)
    language: str = Field(default="en", pattern="^(en|ja|es|fr)$")

class GreetingResponse(BaseModel):
    """レスポンスDTO: APIレスポンスの構造を定義"""
    message: str = Field(..., description="The greeting message")
```