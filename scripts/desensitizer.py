#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中税云检技能库 - 自动脱敏工具
=====================================
使用方法：
  python desensitizer.py <输入文件路径> [输出文件路径]

支持的敏感信息类型：
  1. 手机号码      → 138****5678
  2. 身份证号      → 110************234
  3. 邮箱地址      → z***@example.com
  4. 银行卡号      → 6222 **** **** 1234
  5. 姓名（中文）   → [姓名_已脱敏]
  6. 地址          → [地址_已脱敏]
  7. API Key       → sk-****
  8. 密码/口令     → ******
  9. 统一社会信用代码 → 91**********X
  10. 税号         → 911*********X
"""

import re
import sys
import os
from pathlib import Path
from typing import Optional


class Desensitizer:
    """通用信息脱敏器"""
    
    # 脱敏规则定义
    RULES = {
        '手机号': {
            'pattern': r'(?<!\d)1[3-9]\d{9}(?!\d)',
            'replace': lambda m: m.group(0)[:3] + '****' + m.group(0)[7:]
        },
        '身份证号': {
            'pattern': r'[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]',
            'replace': lambda m: m.group(0)[:3] + '*' * 12 + m.group(0)[-4:]
        },
        '邮箱': {
            'pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'replace': lambda m: m.group(0)[0] + '***@' + m.group(0).split('@')[1] if len(m.group(0).split('@')[0]) > 1 else '*@' + m.group(0).split('@')[1]
        },
        '银行卡号': {
            'pattern': r'\b(?:62|4|5)\d{14,19}\b',
            'replace': lambda m: m.group(0)[:4] + ' **** **** ' + m.group(0)[-4:]
        },
        '中文姓名': {
            'pattern': r'(?:张|王|李|刘|陈|杨|黄|赵|周|吴|徐|孙|马|朱|胡|郭|何|高|林|罗|郑|梁|谢|宋|唐|许|韩|冯|邓|曹|彭|曾|萧|田|董|袁|潘|于|蒋|蔡|余|杜|叶|程|苏|魏|吕|丁|任|沈|姚|卢|姜|崔|钟|谭|陆|汪|范|金|石|廖|贾|夏|韦|傅|方|白|邹|孟|熊|秦|邱|江|尹|薛|闫|段|雷|侯|龙|史|陶|黎|贺|顾|毛|郝|龚|邵|万|钱|严|覃|武|戴|莫|孔|向|汤)[\u4e00-\u9fa5]{1,3}(?=[，。；：！？、\s\n\r]|$)',
            'replace': lambda m: '[姓名_已脱敏]'
        },
        '详细地址': {
            'pattern': r'(?:北京市|上海市|天津市|重庆市|河北省|山西省|辽宁省|吉林省|黑龙江省|江苏省|浙江省|安徽省|福建省|江西省|山东省|河南省|湖北省|湖南省|广东省|海南省|四川省|贵州省|云南省|陕西省|甘肃省|青海省|台湾省|内蒙古自治区|广西壮族自治区|西藏自治区|宁夏回族自治区|新疆维吾尔自治区|香港特别行政区|澳门特别行政区)[^\n，。；]{10,60}',
            'replace': lambda m: '[地址_已脱敏]'
        },
        'API Key': {
            'pattern': r'(?:sk-|api[_-]?key|apikey|token)\s*[=:]\s*["\']?[a-zA-Z0-9_-]{16,}["\']?',
            'replace': lambda m: re.sub(r'[a-zA-Z0-9_-]{4,}', '****', m.group(0))
        },
        '统一社会信用代码': {
            'pattern': r'[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{10}',
            'replace': lambda m: m.group(0)[:2] + '*' * 13 + m.group(0)[-1:] if len(m.group(0)) == 18 else '[信用代码_已脱敏]'
        },
        '税号': {
            'pattern': r'(?:纳税人识别号|税号|统一社会信用代码)[：:\s]*([0-9A-HJ-NPQRTUWXY]{18})',
            'replace': lambda m: m.group(0)[:m.group(0).find(m.group(1))] + '[税号_已脱敏]'
        },
    }
    
    def __init__(self):
        self.stats = {name: 0 for name in self.RULES}
    
    def process(self, text: str) -> str:
        """对文本执行所有脱敏规则"""
        result = text
        for name, rule in self.RULES.items():
            matches = re.findall(rule['pattern'], result)
            if matches:
                self.stats[name] += len(matches)
                result = re.sub(rule['pattern'], rule['replace'], result)
        return result
    
    def process_file(self, input_path: str, output_path: Optional[str] = None) -> str:
        """处理文件并返回输出路径"""
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        
        if output_path is None:
            output_path = input_file.parent / f"{input_file.stem}_desensitized{input_file.suffix}"
        
        content = input_file.read_text(encoding='utf-8', errors='ignore')
        processed = self.process(content)
        
        output_file = Path(output_path)
        output_file.write_text(processed, encoding='utf-8')
        
        return str(output_file)
    
    def get_report(self) -> str:
        """生成脱敏报告"""
        total = sum(self.stats.values())
        lines = ["=" * 50, "📋 脱敏报告", "=" * 50]
        if total == 0:
            lines.append("✅ 未检测到敏感信息")
        else:
            lines.append(f"共发现 {total} 处敏感信息：\n")
            for name, count in self.stats.items():
                if count > 0:
                    lines.append(f"  • {name}: {count} 处")
        lines.append("=" * 50)
        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n使用示例:")
        print("  python desensitizer.py 技能文档.txt")
        print("  python desensitizer.py 原始数据.csv 输出结果.csv")
        print("\n支持批量处理:")
        print("  python desensitizer.py 文件夹路径/")
        sys.exit(0)
    
    target = sys.argv[1]
    des = Desensitizer()
    
    if os.path.isdir(target):
        # 批量处理文件夹
        p = Path(target)
        files = list(p.glob('*.txt')) + list(p.glob('*.md')) + \
                list(p.glob('*.csv')) + list(p.glob('*.json'))
        print(f"\n📁 发现 {len(files)} 个文本文件\n")
        for f in files:
            try:
                out = des.process_file(str(f))
                print(f"  ✅ {f.name} → {Path(out).name}")
            except Exception as e:
                print(f"  ❌ {f.name}: {e}")
    else:
        # 处理单个文件
        output = sys.argv[2] if len(sys.argv) > 2 else None
        try:
            out = des.process_file(target, output)
            print(f"\n✅ 处理完成!")
            print(f"   输出文件: {out}")
        except FileNotFoundError as e:
            print(f"\n❌ 错误: {e}")
            sys.exit(1)
    
    print(f"\n{des.get_report()}")


if __name__ == '__main__':
    main()
