# 进项发票异常检测规则

## 基本信息
- **规则编号**: RULE-VAT-00001
- **适用税种**: 增值税
- **风险等级**: 🔴 高
- **最后更新**: 2026-08-02

---

## 检测逻辑概述

本规则用于识别企业进项发票中的异常模式，包括但不限于：
1. 发票金额异常集中
2. 开票时间规律性异常
3. 销方与购方关联度异常
4. 税率使用错误

---

## 详细检测步骤

### 步骤一：数据提取

**数据源**: 增值税进项发票明细表

**关键字段**:
```
- invoice_id: 发票代码+号码
- issue_date: 开票日期
- seller_name: 销方名称
- buyer_name: 购方名称
- amount: 不含税金额
- tax_amount: 税额
- total_amount: 价税合计
- tax_rate: 税率
- goods_name: 货物/服务名称
```

### 步骤二：异常指标计算

#### 指标1：单张发票金额阈值检测

```python
def check_single_invoice_threshold(amount, industry_avg, threshold=5):
    """
    检测单张发票金额是否超过行业平均值的N倍
    
    参数:
        amount: 单张发票金额
        industry_avg: 行业平均单张发票金额
        threshold: 阈值倍数（默认5倍）
    
    返回:
        bool: 是否异常
    """
    return amount > industry_avg * threshold
```

**脱敏示例**:
| 字段 | 原始值 | 脱敏后 |
|------|--------|--------|
| 发票号码 | 12345678 | 12****78 |
| 金额(元) | 500,000.00 | 500,000.00 |
| 销方名称 | [某科技有限公司] | [企业_已脱敏] |
| 购方名称 | [某商贸有限公司] | [企业_已脱敏] |

#### 指标2：开票时间聚集度检测

```sql
-- SQL 示例：检测同一销方短时间内密集开票
SELECT 
    seller_name,
    COUNT(*) as invoice_count,
    DATE(issue_date) as issue_day,
    SUM(total_amount) as daily_total
FROM input_invoices
WHERE issue_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY seller_name, DATE(issue_date)
HAVING COUNT(*) >= 10  -- 同一天同一销方超过10张
   OR SUM(total_amount) >= 1000000  -- 日累计超100万
ORDER BY daily_total DESC;
```

#### 指标3：税率匹配校验

```python
TAX_RATE_RULES = {
    '货物销售': {13, 9},      # 一般货物
    '交通运输': {9},          # 运输服务
    '现代服务': {6},          # 服务业
    '不动产租赁': {9, 5},     # 租赁
}

def validate_tax_rate(goods_category, actual_rate):
    """校验税率是否与货物类别匹配"""
    expected_rates = TAX_RATE_RULES.get(goods_category, set())
    return actual_rate in expected_rates if expected_rates else True
```

---

## 风险等级判定

| 异常类型 | 触发条件 | 风险等级 | 处置建议 |
|---------|---------|---------|---------|
| 大额单票 | 单张≥行业均值×10倍 | 🔴高 | 立即人工复核 |
| 密集开票 | 同销方日开票≥20张 | 🔴高 | 启动专项检查 |
| 税率错配 | 税率与品目不匹配 | 🟡中 | 标记待核实 |
| 时间异常 | 非工作时间批量开票 | 🟡中 | 关注备注 |
| 金额突增 | 月环比增长>300% | 🟡中 | 分析原因 |

---

## 输出格式

检测结果输出为结构化 JSON：

```json
{
  "rule_id": "RULE-VAT-00001",
  "execute_time": "2026-08-02T10:30:00Z",
  "taxpayer_id": "[纳税人识别号_已脱敏]",
  "risk_items": [
    {
      "type": "LARGE_INVOICE",
      "severity": "HIGH",
      "invoice_id": "***",
      "amount": 500000.00,
      "description": "单张发票金额超过行业平均值8倍"
    }
  ],
  "total_risk_score": 85,
  "recommendation": "建议立即开展人工核实"
}
```

---

## 配置参数

可在配置文件中调整以下参数：

```yaml
detection_params:
  single_invoice_multiplier: 5      # 单票金额阈值倍数
  daily_invoice_count_limit: 20     # 日开票数量上限
  daily_amount_limit: 1000000       # 日开票金额上限(元)
  month_growth_rate_limit: 3.0      # 月环比增长率上限
  off_hours_start: 22               # 非工作时段起始
  off_hours_end: 6                  # 非工作时段结束
```

---

*本规则由中税云检系统自动生成，案例数据已全部脱敏*
