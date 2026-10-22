# Requirement Planner

Requirement Planner 是一個可安裝到 AI agent 的 skill，用來將 Jira issue、
需求網址、ticket 或產品需求整理成可直接交給 Coding Agent 的實作規格。
它會透過執行 Agent 當下可用的需求來源能力取得需求、檢查目前專案、只詢問會影響實作的問題，並在修改產品程式碼
之前產生規劃文件。

產生的文件位置：

```text
docs/requirements/<REQUIREMENT_KEY>/
├── SOURCE_SNAPSHOT.md
├── IMPLEMENTATION_SPEC.md
└── TEST_REQUIREMENTS.md
```

所有規格文件與測試需求都會使用繁體中文。

## 需求來源存取

遇到 Jira URL 時，Agent 一律使用當下可用、且經使用者授權的瀏覽器。
先檢查既有分頁，有符合網址的分頁就優先使用；沒有才開啟使用者提供的連結。
不執行舊 Jira API 腳本，也不檢查 `.env` 或本地帳密。本專案不提供瀏覽器實作，
也不再要求 Jira 帳號、密碼、API token、cookie 或公司 CA 路徑。

若頁面要求登入，請在 Agent 提供的介面完成登入，再由 Agent 重新載入並確認原始
Issue URL。不要把憑證貼到聊天中。若沒有可用的來源能力，請改提供貼上的需求、
export、截圖、PDF 或文件。

## 安裝與使用

### Codex

在目標專案中執行：

```text
$skill-installer install https://github.com/<owner>/<repo>/tree/main/skills/requirement-planner
```

重新啟動 Codex 後使用：

```text
$requirement-planner
Please plan implementation for this Jira requirement:
https://jira.example.com/browse/APP-1234
```

## 規劃行為

Agent 會先檢查需求來源與目前專案，再釐清會影響需求理解、實作範圍或驗收的
重要不確定事項。問題數量沒有固定上限；Agent 會避免重複詢問已有證據可回答的
內容，並在答案帶出新的重要不確定事項時繼續追問。若來源或專案證據不存在，會
明確標示未知，不會為了符合問題格式而編造證據或選項。阻塞問題解決並經使用者
確認後，才會將規格標記為可開始實作。

### Cursor

Cursor 會從 `~/.cursor/skills/` 與 `~/.agents/skills/` 掃描使用者 skill。
安裝到 Cursor 個人 skill 目錄：

```bash
git clone https://github.com/<owner>/<repo>.git requirement-planner-repo
mkdir -p ~/.cursor/skills
cp -R requirement-planner-repo/skills/requirement-planner ~/.cursor/skills/
```

重新啟動 Cursor 後，可以使用 `/requirement-planner`，或讓 Cursor 根據需求
描述自動選擇此 skill。

### Claude Code

Claude Code 會從 `~/.claude/skills/` 掃描使用者 skill：

```bash
git clone https://github.com/<owner>/<repo>.git requirement-planner-repo
mkdir -p ~/.claude/skills
cp -R requirement-planner-repo/skills/requirement-planner ~/.claude/skills/
```

重新啟動 Claude Code 後，可以使用 `/requirement-planner`，或讓它根據需求
自動選擇此 skill。

### Gemini CLI

Gemini CLI 可以直接從 repository URL 安裝：

```bash
gemini skills install https://github.com/<owner>/<repo>.git --path skills/
```

安裝後重新載入 Gemini CLI，確認可用 skills 中出現
`requirement-planner`。如果要控制安裝到使用者或目前 workspace，請依 Gemini
CLI 版本使用對應的 scope 選項。

### 其他支援 `SKILL.md` 的 AI agent

不需要複製整個專案，只要取得 `skills/requirement-planner/`。其中的
`SKILL.md`、`scripts/`、`references/`、`schemas/` 與 `templates/`
必須一起保留，再依該 agent 的規則放到它的 skills 目錄，最後重新啟動 agent。

### 不支援原生 skill 的 AI agent

將 skill 複製到目標專案後，在 agent 的專案指示檔加入：

```text
When planning a requirement, read .agents/skills/requirement-planner/SKILL.md and
follow it exactly. Use only the available user-authorized browser tools for URL
requirements, and use the Python scripts in that skill only for inspection,
validation, and clear docs operations.
```

## 清除已產生的規格文件

完成規格審閱或想重新開始時，輸入：

```text
$requirement-planner clear docs
```

這會刪除所有 requirement key 資料夾底下由工具產生的：

- `SOURCE_SNAPSHOT.md`
- `IMPLEMENTATION_SPEC.md`
- `TEST_REQUIREMENTS.md`

不會刪除 `docs/requirements/` 本身，也不會刪除 `docs/` 裡的其他檔案。
