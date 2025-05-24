#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本 - 测试tu-zi.com API是否正常工作
"""

import json
import requests

# API配置
API_URL = "https://api.tu-zi.com/v1/chat/completions"
API_KEY = "sk-uHuYUvSiN3xbHBKhmQ9Yf6Zucbv6T3YRvG5VqjKfeObB5H8u"

def test_api():
    """测试API连接和功能"""
    print("🧪 开始测试API...")
    print(f"API地址: {API_URL}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system", 
                "content": "你是一位专业的活动策划专家，请为给定的组合创作一个简短的活动标题。"
            },
            {
                "role": "user", 
                "content": "请为以下维度组合创作一个活动标题：地域：山东、种类：舞蹈、品种：拉丁舞、活动类型：比赛"
            }
        ],
        "max_tokens": 50,
        "temperature": 0.8
    }
    
    try:
        print("📡 发送API请求...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            title = result['choices'][0]['message']['content'].strip()
            print(f"✅ API测试成功！")
            print(f"🎯 生成的标题: {title}")
            return True
        else:
            print(f"❌ API调用失败")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        return False

def test_with_combinations():
    """使用测试组合文件测试"""
    print("\n" + "="*50)
    print("🔬 使用测试组合进行完整测试...")
    
    try:
        with open('test_combinations.json', 'r', encoding='utf-8') as f:
            combinations = json.load(f)
        
        print(f"📋 加载了 {len(combinations)} 个测试组合")
        
        from generate_titles import TitleGenerator
        
        generator = TitleGenerator()
        
        for i, combo in enumerate(combinations, 1):
            print(f"\n🧪 测试组合 {i}/{len(combinations)}")
            combo_str = " | ".join([f"{k}: {v}" for k, v in combo.items()])
            print(f"组合: {combo_str}")
            
            user_prompt = generator.create_user_prompt(combo)
            title = generator.call_api(user_prompt)
            
            print(f"生成标题: {title}")
            
        print("\n✅ 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    print("🎯 tu-zi.com API 测试工具")
    print("="*40)
    
    # 基础API测试
    if test_api():
        # 如果基础测试通过，进行完整测试
        test_with_combinations()
    else:
        print("\n❌ 基础API测试失败，请检查API配置") 