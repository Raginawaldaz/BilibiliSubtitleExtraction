# SubtitleExtraction

从 B 站视频（含多分 P）提取 CC 字幕，并保存为本地 `.txt` 文件。

## 环境要求

- Python 3.10+
- 已登录 B 站账号的 Cookie（部分视频需登录才能拉到字幕）

## 快速开始

```powershell
# 1. 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. 安装依赖
pip install bilibili-api-python python-dotenv requests

# 3. 配置环境变量
copy .env.example .env
# 编辑 .env：填入 BILIBILI_COOKIE，以及目标 BV / 视频链接
```

### Cookie 怎么拿

1. 浏览器登录 [bilibili.com](https://www.bilibili.com)
2. 打开开发者工具 → Network，刷新任意页面
3. 任选一条请求，复制请求头里的整段 `Cookie`
4. 粘贴到 `.env` 的 `BILIBILI_COOKIE`（外层用双引号）

### 目标视频怎么填

在 `.env` 里设置 `BILIBILI_VIDEO`，支持两种写法：

```env
BILIBILI_VIDEO=BV1NkM66LEwX
# 或
BILIBILI_VIDEO=https://www.bilibili.com/video/BV1NkM66LEwX
```

改完保存即可，无需改 Python 代码。

## 运行

```powershell
python get_bilibili_subs.py
```

字幕按 BV 号分类输出，结构如下：

```text
subtitles/
  BV1NkM66LEwX/
    P01_分P标题.txt
    P02_分P标题.txt
    ...
```

## 配置说明

| 变量 | 说明 |
|------|------|
| `BILIBILI_COOKIE` | 浏览器整段 Cookie，需含 `SESSDATA`、`bili_jct` 等 |
| `BILIBILI_VIDEO` | BV 号或完整视频 URL |

完整模板见 [`.env.example`](.env.example)。本地实际配置写在 `.env`（已加入 `.gitignore`，勿提交）。

## 说明

- 仅提取官方 CC / 投稿字幕；无字幕的分 P 会打印「未获取到字幕数据」
- Cookie 过期后重新从浏览器复制即可

## License

本项目采用 [Apache License 2.0](LICENSE)。
