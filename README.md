# Shipber 现场实操题库

用于测试开发与全栈研发岗位的现场实操。按岗位分目录，每套题独立保存题面、运行项目和合成样例。

## 目录

| 岗位 | 目录 | 当前题目 |
| --- | --- | --- |
| 测试开发 | [test-development](test-development/README.md) | [报价金额验证，30 分钟](test-development/quote-validation-30m/TASK.md) |
| 全栈研发 | [fullstack](fullstack/README.md) | 待添加 |

## 使用

选择对应题目，将该题目录提供给候选人。测试开发题允许使用 AI 和公开文档，面试官在旁观察；具体要求以题面为准。

现有报价项目只需 Python 3.10+，无需安装依赖、连接数据库或配置账号：

```sh
cd test-development/quote-validation-30m
python3 quote_service.py
```

服务启动在 `http://127.0.0.1:8765`。另开终端进入同一目录执行：

```sh
curl -s -H 'Content-Type: application/json' --data-binary @example.json http://127.0.0.1:8765/quote
```

正常样例合计为 `13.20`。端口占用可指定 `--port 8766`；端口受限时可执行 `python3 quote_service.py --quote-file example.json`。结束后 Ctrl+C 停止服务。

## 内容边界

本仓库内容可向候选人提供，不存放面试官答案、内部评价标准、临场追加问题或候选人作答记录。代码和数据均用于面试演示，不连接真实业务，也不应部署到生产。

新增题目按 `<岗位>/<题目名称>/` 保存，并在岗位索引中说明版本、时长、允许工具及运行要求。候选人的提交和个人资料保存在另外指定的位置。
