# 使用指南

## 快速上手

### 方式一：网页端操作（推荐新手）

1. 打开仓库页面：https://github.com/leewu80/zhongshui-cloud-skills
2. 点击 **「Add file」→「Create new file」** 创建新文件
3. 编写或粘贴内容（确保已脱敏）
4. 填写提交信息，点击 **「Commit changes」**

### 方式二：GitHub Desktop（推荐日常使用）

1. 打开 GitHub Desktop 应用
2. 登录你的 GitHub 账号 (leewu80)
3. 点击 **File → Clone repository**
4. 选择 `zhongshui-cloud-skills` 仓库
5. 选择本地保存位置，点击 **Clone**
6. 在本地文件夹中添加/编辑文件
7. 在 GitHub Desktop 中填写提交信息
8. 点击 **Commit to main** 然后 **Push origin**

### 方式三：命令行 Git（推荐开发者）

```bash
git clone https://github.com/leewu80/zhongshui-cloud-skills.git
cd zhongshui-cloud-skills
git checkout -b add-new-skill
git add .
git commit -m "新增技能文档"
git push origin add-new-skill
```

## 文件命名规范

推荐格式: `vat-invoice-check.md` (小写英文+连字符)
避免: 中文文件名、空格、特殊字符

## 目录约定

| 目录 | 用途 |
|-----|------|
| skills/tax-detection/ | 税务检测规则 |
| skills/data-process/ | 数据处理流程 |
| scripts/ | 工具脚本 |
| docs/ | 文档资料 |

## 常见问题

Q: 如何确认文件已脱敏？
A: 运行 `python scripts/desensitizer.py <文件>` 检查

Q: 可以上传 Excel/Word 吗？
A: 可以，但推荐转为 Markdown 格式

Q: 如何删除误传文件？
A: 在网页找到文件，点击删除按钮提交即可
