#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
组合生成器
读取维度配置文件，生成所有可能的组合
"""

import json
import itertools
import os
from pathlib import Path

def load_dimensions():
    """加载维度配置文件"""
    config_file = "config/dimensions.json"
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['dimensions']
    except FileNotFoundError:
        print(f"错误：配置文件 {config_file} 未找到")
        exit(1)
    except json.JSONDecodeError:
        print(f"错误：配置文件 {config_file} 格式错误")
        exit(1)

def generate_combinations(dimensions):
    """生成所有维度的组合"""
    dimension_names = list(dimensions.keys())
    dimension_values = list(dimensions.values())
    
    combinations = list(itertools.product(*dimension_values))
    
    formatted_combinations = []
    for combo in combinations:
        combo_dict = dict(zip(dimension_names, combo))
        formatted_combinations.append(combo_dict)
    
    return formatted_combinations

def save_combinations(combinations):
    """保存组合到文件"""
    output_file = "combinations.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combinations, f, ensure_ascii=False, indent=2)
    
    print(f"组合已保存到: {output_file}")

def main():
    print("正在加载维度配置...")
    dimensions = load_dimensions()
    
    print(f"发现 {len(dimensions)} 个维度：")
    for dim_name, options in dimensions.items():
        print(f"  - {dim_name}: {len(options)} 个选项")
    
    print("\n正在生成组合...")
    combinations = generate_combinations(dimensions)
    
    print(f"生成完成！总共 {len(combinations)} 个组合")
    
    save_combinations(combinations)
    
    # 显示前几个组合示例
    print(f"\n组合示例（前5个）：")
    for i, combo in enumerate(combinations[:5], 1):
        combo_str = " | ".join([f"{k}: {v}" for k, v in combo.items()])
        print(f"{i}. {combo_str}")
    
    if len(combinations) > 5:
        print(f"... 还有 {len(combinations) - 5} 个组合")

if __name__ == "__main__":
    main() 