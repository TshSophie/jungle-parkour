# 丛林跑酷 · 健身版

用身体动作（左右探身 / 向上弹跳 / 下蹲）操控角色在原始丛林里躲避障碍，边玩边活动颈肩、缓解久坐疲劳的轻量健身小游戏。纯前端、零后端、本地模型推理（MediaPipe Face Landmarker），数据不出本机。

## 版本

- `jungle-parkour-mobile.html` —— 手机版：底部触摸按钮操控，或开启前置摄像头用身体动作玩。
- `jungle-parkour-demo.html` —— 桌面版：笔记本摄像头识别头部姿态操控（左右歪头换道、抬头/低头弹跳下蹲）。
- `jungle-parkour-3d.html` —— 高仿真 3D 验证版（Three.js）：程序化丛林（雾效/阴影/纵深）+ 会从树后突然窜出伏击的怪兽；输入/检测/校准层与桌面版完全一致，仅渲染层升级为 WebGL。
- `index.html` —— 落地页，含各版本入口。
- `lib/` —— 本地 MediaPipe 模型与 wasm 运行时（含 `face_landmarker.task`），保证离线可用、不依赖 CDN。
- `lib/three/` —— 本地 Three.js（r160），供 3D 版离线使用。

## 本地运行

任意静态服务器均可，例如：

```bash
python -m http.server 8000
# 浏览器打开 http://127.0.0.1:8000/index.html
```

- 桌面摄像头：`http://127.0.0.1:8000/jungle-parkour-demo.html`（localhost 下摄像头可用）。
- 手机同 Wi-Fi 访问：将 `127.0.0.1` 换成本机局域网 IP；摄像头需 HTTPS，见下。

## 部署到 Gitee Pages（免费、自带 HTTPS）

1. 新建公开仓库，把本目录（含 `lib/`）推送到 `master` 分支。
2. 仓库内「服务 → Gitee Pages」，部署分支选 `master`，点击启动。
3. 访问 `https://<用户名>.gitee.io/<仓库名>/index.html`。
4. 因 Pages 为 HTTPS，朋友的摄像头模式可直接使用，无需自签证书。

> 注意：必须用 Pages 生成的站点地址，不要用「原始文件 / raw」链接（无目录上下文，`lib/` 加载会失败）。公开仓库意味着任何拿到链接的人都能试玩；校准数据保存在各自浏览器 localStorage，互不干扰。

## 远程给朋友试玩（无需云服务器）

- 最简：部署到 Gitee Pages 后，把站点链接发给朋友即可（HTTPS，摄像头可用）。
- 临时：用 Cloudflare Tunnel / ngrok 把本地服务暴露为公网 HTTPS 链接；或更私密地用 Tailscale 组虚拟局域网（HTTP，仅触摸模式）。
