# Zepp 步数修改器 (Zepp Steps)

基于 Zepp API 的自动步数修改工具。通过模拟 Zepp 的数据同步请求，实现一键修改微信运动、支付宝等平台的每日步数。

## ✨ 特性

- **现代化 UI**: 采用玻璃拟态（Glassmorphism）和动态背景的极简前端设计。
- **一键修改**: 输入账号、密码及目标步数，即可快速完成同步。
- **双向数据绑定**: 支持滑块快捷调整步数，也支持直接手动输入精准步数。
- **Serverless 架构**: 后端基于 Python，完美适配 Vercel Zero Config 零配置一键部署。

## 🚀 部署指南 (Vercel)

本项目专为 Vercel 优化，支持一键零配置部署：

1. **Fork 本仓库** 到你的 GitHub 账号。
2. 登录 [Vercel](https://vercel.com/)，点击 **Add New -> Project**。
3. 选择刚才 Fork 的 `zepp-step` 仓库并点击 **Import**。
4. **无需任何额外配置**（保持 Framework Preset 为 Other），直接点击 **Deploy**。
5. 部署完成后，访问 Vercel 分配的域名即可使用。

*注意：请确保项目根目录下不要包含 `pyproject.toml` 或 `vercel.json`，以免干扰 Vercel 的原生路由策略。本项目的 Python 后端依赖已配置在 `api/requirements.txt` 中。*

## 📁 目录结构

```text
├── api/
│   ├── requirements.txt   # 后端 Python 依赖配置
│   ├── steps.py           # 核心步数修改 API 接口
│   └── zepp_login.py      # Zepp Life 登录鉴权逻辑
└── index.html             # 前端交互页面
```

## ⚠️ 免责声明

1. 本项目**仅供编程学习与技术研究**使用。
2. 请勿将本项目用于任何商业用途或非法用途。
3. 因使用本项目而导致的任何账号异常、封禁或其他损失，由使用者自行承担责任。

---
*Made with ❤️ by CMontage*
