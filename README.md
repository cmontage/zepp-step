# Zepp 步数修改器 (Zepp Steps)

基于 Zepp API 的自动步数修改工具。通过模拟 Zepp 的数据同步请求，实现一键修改微信运动、支付宝等平台的每日步数。

> [!TIP]
> 1. 您的 Zepp 账号**必须**绑定过任意一款穿戴设备（只要绑定过即可，无论设备是否在线），否则无法向服务器成功同步步数。
> 2. 微信 / 支付宝只需要在 Zepp App 内绑定第三方接入，即可自动同步修改后的步数。

<div align="center">
  <img src="https://gcore.jsdelivr.net/gh/cmontage/zepp-step@main/img/simple.png" alt="Zepp Steps Preview" width="600"/>
</div>

## ✨ 特性

- **现代化 UI**: 采用玻璃拟态（Glassmorphism）和动态背景的极简前端设计。
- **精准修改**: 输入框、滑块与随机生成均支持精准到**个位数**的步数修改。
- **一键修改**: 输入账号、密码及目标步数，即可快速完成同步。
- **Serverless 架构**: 后端基于 Python，完美适配 Vercel Zero Config 零配置一键部署。
- **原生 Docker 支持**: 内置轻量级 Web 服务器，支持 NAS 及本地容器化一键部署。

## 🚀 部署指南

### 方式一：Vercel (零配置一键部署)
本项目专为 Vercel 优化：
1. **Fork 本仓库** 到你的 GitHub 账号。
2. 登录 [Vercel](https://vercel.com/)，点击 **Add New -> Project**。
3. 选择刚才 Fork 的 `zepp-step` 仓库并点击 **Import**。
4. **无需任何额外配置**（保持 Framework Preset 为 Other），直接点击 **Deploy**。
5. 部署完成后，访问 Vercel 分配的域名即可使用。
*注意：请确保项目根目录下不要包含 `pyproject.toml` 或 `vercel.json`。*

### 方式二：Docker / NAS 部署 (本地化部署)
针对 NAS（如飞牛 OS）或本地服务器环境，项目内置了 Docker 部署支持：
1. 下载/克隆本仓库到本地。
2. 进入 `compose` 目录，或者在根目录下运行构建命令：
   ```bash
   docker-compose -f compose/docker-compose.yml up -d --build
   ```
3. 容器启动后，在浏览器中访问映射的端口（默认为 `11400`），即可进入修改页面。

### 方式三：原生 Python 部署 (服务器/本地裸机部署)
如果你不想使用 Docker，也可以直接通过 Python 运行内置的 Web 服务器：
1. 下载/克隆本仓库到本地服务器或电脑。
2. 安装环境依赖（建议使用 Python 3.7+）：
   ```bash
   pip install -r api/requirements.txt
   ```
3. 启动服务器（需确保当前在项目根目录）：
   ```bash
   # Linux / macOS
   PYTHONPATH=$PWD python compose/server.py

   # Windows
   set PYTHONPATH=%CD%&& python compose/server.py
   ```
4. 启动成功后，打开浏览器访问 `http://127.0.0.1:11400` 或服务器对应 IP 的 `11400` 端口即可。

## 🆕 最近更新
- **Fix (API)**: 深度修复并重构了华米接口 `data_json` 的 Payload 打包逻辑，采用原生无损转义（Raw String）格式，彻底解决 NAS 或本地独立容器部署时频繁出现的 `400 Bad Request` 报错。
- **Fix (UI)**: 移除了前端页面（输入框、滑块）只能按 100 步递增的限制，全面支持个位数级精准调整，包含随机生成算法也调整为了精确到个位数的随机值。

## 📁 目录结构

```text
├── api/
│   ├── requirements.txt   # 后端 Python 依赖配置
│   ├── steps.py           # 核心步数修改 API 接口
│   └── zepp_login.py      # Zepp 登录鉴权逻辑
├── compose/
│   ├── Dockerfile         # 容器化构建配置
│   ├── docker-compose.yml # Docker Compose 编排文件
│   └── server.py          # 本地/容器内置轻量 HTTP 服务器
└── index.html             # 前端交互页面
```

## ⚠️ 免责声明

1. 本项目**仅供编程学习与技术研究**使用。
2. 请勿将本项目用于任何商业用途或非法用途。
3. 因使用本项目而导致的任何账号异常、封禁或其他损失，由使用者自行承担责任。

---
*Made with ❤️ by CMontage*
