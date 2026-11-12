# Shipber 现场实操题库

欢迎参加 Shipber 技术面试。本仓库提供现场实操的题目、示例项目和样例数据，请根据面试安排进入对应岗位目录。

## 目录

| 岗位 | 目录 | 当前题目 |
| --- | --- | --- |
| 测试开发 | [test-development](test-development/README.md) | [报价金额验证，30 分钟](test-development/quote-validation-30m/TASK.md) |
| 全栈研发 | [fullstack](fullstack/README.md) | 暂未发布 |

## 开始之前

请先阅读对应题目的 `TASK.md`，了解业务规则、任务要求、时间安排和交付内容。允许使用的工具以题面为准；当前测试开发题允许使用 AI 和公开文档，也可以完全不使用 AI。

实操过程中，请保留实际运行结果，并准备说明你的思路、关键判断和验证过程。遇到题意或环境问题，可以随时向面试官提出。

## 运行报价示例

下载或克隆本仓库后，在仓库根目录执行以下命令。报价项目需要 Python 3.10+，无需安装第三方依赖、连接数据库或配置账号：

```sh
cd test-development/quote-validation-30m
python3 quote_service.py
```

服务启动在 `http://127.0.0.1:8765`。另开终端进入同一目录执行：

```sh
curl -s -H 'Content-Type: application/json' --data-binary @example.json http://127.0.0.1:8765/quote
```

正常样例合计为 `13.20`。端口占用可指定 `--port 8766`；端口受限时可执行 `python3 quote_service.py --quote-file example.json`。结束后 Ctrl+C 停止服务。

## 提交方式

按照题面要求整理代码、运行命令和结果，通过面试官指定的方式提交。请勿将作答或个人信息提交到本公开仓库的 Issue 或 Pull Request。

题目使用合成业务和样例数据，仅用于实操。使用 AI 或补充样例时，请勿引入真实客户数据、账号凭据或前雇主的保密材料。
