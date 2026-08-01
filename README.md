# 中税云检技能库 🛡️

> **中税云智能税务检测** 技能集合与知识库

## 📋 项目简介

本仓库用于存储和管理中税云检相关的专业技能、检测规则、数据处理脚本和最佳实践文档。

所有文件均经过**敏感信息脱敏处理**，确保数据安全。

---

## 📁 目录结构

```
zhongshui-cloud-skills/
├── README.md              # 项目说明文件
├── .gitignore             # Git 忽略规则
├── skills/                # 技能规则库
│   ├── tax-detection/     # 税务检测规则
│   ├── data-process/      # 数据处理流程
│   └── risk-assessment/   # 风险评估模型
├── scripts/               # 自动化脚本
│   └── desensitizer.py    # 脱敏工具
├── docs/                  # 文档资料
│   └── usage-guide.md     # 使用指南
└── templates/             # 模板文件
```

## 🔒 脱敏说明

### 已处理的敏感信息类型

| 类型 | 脱敏规则 | 示例 |
|------|---------|------|
| 手机号 | 保留前3后4位 | `138****5678` |
| 身份证号 | 保留前3后4位 | `110************234` |
| 邮箱 | 隐藏用户名 | `z***@example.com` |
| 中文姓名 | 完全替换 | `[姓名_已脱敏]` |
| 地址信息 | 完全替换 | `[地址_已脱敏]` |
| API Key | 隐藏关键部分 | `sk-****` |
| 统一信用代码 | 部分隐藏 | `91**********X` |

### 使用脱敏工具

```bash
# 处理单个文件
python desensitizer.py 原始文件.txt

# 批量处理文件夹
python desensitizer.py ./待处理文件夹/

# 指定输出路径
python desensitizer.py input.csv output_desensitized.csv
```

## 🚀 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/leewu80/zhongshui-cloud-skills.git
   cd zhongshui-cloud-skills
   ```

2. **查看技能文档**
   ```bash
   ls skills/
   cat skills/tax-detection/README.md
   ```

3. **添加新技能**
   ```bash
   # 先用脱敏工具处理
   python scripts/desensitizer.py 你的新技能.md
   
   # 然后提交
   git add .
   git commit -m "添加新技能：xxx"
   git push
   ```

## 📌 注意事项

⚠️ **上传前请务必确认：**

- [ ] 所有个人身份信息已脱敏
- [ ] 手机号码已隐藏中间4位
- [ ] 身份证号已做掩码处理
- [ ] 企业名称如需保密已替换
- [ ] 地址信息已模糊化
- [ ] 无明文密码或密钥

## 🤝 贡献指南

欢迎提交新的检测规则和技能文档！请确保：

1. 文件使用 Markdown 格式
2. 内容经过脱敏处理
3. 添加适当的分类目录
4. 更新相关文档索引

## 📄 许可证

本项目仅供内部学习和研究使用，请勿用于商业用途。

---

**维护者**: leewu80  
**最后更新**: 2026-08-02  
**版本**: v1.0.0
