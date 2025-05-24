#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动标题生成器
使用OpenAI GPT-4o API根据维度组合生成创意的运营活动标题
"""

import json
import os
import time
import requests

# API配置
API_CONFIG = {
    "model": "gpt-4o",
    "max_tokens": 50,
    "temperature": 0.8,
    "top_p": 0.9,
    "timeout": 30,
    "max_retries": 3,
    "delay": 1.0
}

# 系统提示词
SYSTEM_PROMPT = """你是一位专业的活动策划和文案专家，擅长创作吸引人的活动标题。

请根据给定的维度组合，创作一个富有创意、朗朗上口的运营活动标题。

要求：
1. 标题要体现所有给定的维度元素
2. 标题要有地域特色和文化内涵
3. 标题要简洁有力，容易记忆
4. 标题要有号召力和吸引力
5. 可以使用押韵、对仗、谐音等修辞手法
6. 字数控制在8-15字之间

请直接输出标题，不要添加任何解释或其他内容。"""

class TitleGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_user_prompt(self, combination):
        """根据组合创建用户提示词"""
        combo_str = "、".join([f"{k}：{v}" for k, v in combination.items()])
        return f"请为以下维度组合创作一个活动标题：\n\n{combo_str}\n\n请结合这些元素的特点，创作一个既有地域特色又突出活动特点的标题。"

    def call_api(self, user_prompt):
        """调用OpenAI API"""
        payload = {
            "model": API_CONFIG["model"],
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": API_CONFIG["max_tokens"],
            "temperature": API_CONFIG["temperature"],
            "top_p": API_CONFIG["top_p"]
        }
        
        for attempt in range(API_CONFIG["max_retries"]):
            try:
                response = requests.post(
                    self.api_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=API_CONFIG["timeout"]
                )
                
                if response.status_code == 200:
                    result = response.json()
                    title = result['choices'][0]['message']['content'].strip()
                    return title
                else:
                    print(f"API调用失败，状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"第 {attempt + 1} 次尝试失败: {str(e)}")
                
            if attempt < API_CONFIG["max_retries"] - 1:
                time.sleep((attempt + 1) * 2)
        
        return f"生成失败_{int(time.time())}"

    def generate_titles(self, combinations):
        """为所有组合生成标题"""
        results = []
        total = len(combinations)
        
        print(f"开始为 {total} 个组合生成标题...")
        print("=" * 50)
        
        for i, combination in enumerate(combinations, 1):
            print(f"\n进度: {i}/{total}")
            
            combo_display = " | ".join([f"{k}: {v}" for k, v in combination.items()])
            print(f"组合: {combo_display}")
            
            user_prompt = self.create_user_prompt(combination)
            
            print("正在生成标题...")
            title = self.call_api(user_prompt)
            
            result = {
                "序号": i,
                "组合": combination,
                "标题": title,
                "生成时间": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
            
            print(f"生成标题: {title}")
            
            if i < total:
                print(f"等待 {API_CONFIG['delay']} 秒...")
                time.sleep(API_CONFIG['delay'])
        
        return results

    def save_results(self, results):
        """保存结果到文件"""
        # 保存JSON格式
        json_file = "generated_titles.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n详细结果已保存到: {json_file}")
        
        # 保存CSV格式
        csv_file = "generated_titles.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("序号,地域,种类,品种,活动类型,生成标题\n")
            for result in results:
                combo = result['组合']
                line = f"{result['序号']},{combo.get('地域', '')},{combo.get('种类', '')},{combo.get('品种', '')},{combo.get('活动类型', '')},{result['标题']}\n"
                f.write(line)
        print(f"CSV格式结果已保存到: {csv_file}")

def load_combinations():
    """加载组合文件"""
    combinations_file = "combinations.json"
    try:
        with open(combinations_file, 'r', encoding='utf-8') as f:
            combinations = json.load(f)
        return combinations
    except FileNotFoundError:
        print(f"错误：组合文件 {combinations_file} 未找到")
        print("请先运行 python generate_combinations.py 生成组合文件")
        exit(1)

def main():
    # 检查API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("请设置 OPENAI_API_KEY 环境变量")
        print("例如: export OPENAI_API_KEY='your-api-key-here'")
        exit(1)
    
    # 加载组合
    print("正在加载组合文件...")
    combinations = load_combinations()
    print(f"加载了 {len(combinations)} 个组合")
    
    # 确认继续
    if len(combinations) > 10:
        confirm = input(f"\n将要生成 {len(combinations)} 个标题，这可能需要一些时间和API费用。是否继续? (y/n): ")
        if confirm.lower() not in ['y', 'yes', '是']:
            print("操作已取消")
            return
    
    # 设置延迟时间
    delay_input = input(f"\n请输入API调用间隔时间（秒，默认{API_CONFIG['delay']}）: ")
    if delay_input:
        try:
            API_CONFIG['delay'] = float(delay_input)
        except ValueError:
            print("使用默认延迟时间")
    
    # 创建生成器并开始生成
    generator = TitleGenerator(api_key)
    results = generator.generate_titles(combinations)
    generator.save_results(results)
    
    print("\n" + "=" * 50)
    print("标题生成完成！")
    print(f"共生成 {len(results)} 个标题")
    
    # 显示示例结果
    print("\n示例结果:")
    for i, result in enumerate(results[:5], 1):
        combo = result['组合']
        combo_str = " + ".join(combo.values())
        print(f"{i}. {combo_str} → {result['标题']}")
    
    if len(results) > 5:
        print(f"... 还有 {len(results) - 5} 个结果")

if __name__ == "__main__":
    main() 