# Cold Lead Finder

自动从 Reddit 和 Hacker News 抓取潜在客户，分析痛点并生成个性化冷邮件模板。

## 功能

- 🔍 关键词监控 Reddit/HN 帖子
- 🤖 AI 分析用户痛点
- ✉️ 自动生成个性化邮件模板
- 📊 导出 CSV 格式客户清单

## 安装


## 配置

### 1. 获取 Reddit API 凭证

1. 访问 https://www.reddit.com/prefs/apps
2. 点击 "create another app"
3. 选择 "script" 类型
4. 记录 `client_id` 和 `client_secret`

### 2. 获取 OpenAI API Key

1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API key

### 3. 设置环境变量


或直接导出：


## 使用

### 基础搜索


### 指定平台


### 自定义输出


### 安装后使用


## 输出格式

CSV 文件包含以下字段：

| 字段 | 说明 |
|------|------|
| platform | 来源平台 (reddit/hackernews) |
| author | 用户名 |
| title | 帖子标题 |
| url | 帖子链接 |
| content | 内容摘要 |
| pain_point | AI 提取的痛点 |
| email_template | 个性化邮件模板 |

## 示例输出


## 注意事项

- Reddit API 有速率限制（60 请求/分钟）
- OpenAI API 按 token 计费
- 建议先小批量测试（limit=10）
- 遵守各平台的使用条款

## 故障排查

**Reddit 认证失败**
- 检查 client_id 和 client_secret 是否正确
- 确认应用类型为 "script"

**OpenAI API 错误**
- 验证 API key 是否有效
- 检查账户余额

**无结果返回**
- 尝试更通用的关键词
- 增加 limit 参数
- 检查网络连接

## License

MIT