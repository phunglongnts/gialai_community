#!/usr/bin/env python3
"""
Script tối ưu Ollama để AI response nhanh hơn
Chạy script này để cấu hình Ollama tối ưu
"""

import subprocess
import sys
import time
import json
import requests


def run_command(command, capture_output=True):
    """Chạy command và trả về kết quả"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True)
            return result.returncode == 0, "", ""
    except Exception as e:
        return False, "", str(e)


def check_ollama_status():
    """Kiểm tra trạng thái Ollama"""
    print("🔍 Kiểm tra Ollama...")

    try:
        response = requests.get("http://127.0.0.1:1234/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama đang chạy với {len(models)} models")
            return True, models
        else:
            print("❌ Ollama không phản hồi")
            return False, []
    except Exception as e:
        print(f"❌ Không thể kết nối Ollama: {e}")
        return False, []


def optimize_ollama_config():
    """Tối ưu cấu hình Ollama"""
    print("\n⚙️ Tối ưu cấu hình Ollama...")

    # Set environment variables for better performance
    env_vars = {
        "OLLAMA_NUM_PARALLEL": "2",  # Số requests parallel
        "OLLAMA_MAX_LOADED_MODELS": "1",  # Chỉ load 1 model để tiết kiệm RAM
        "OLLAMA_FLASH_ATTENTION": "1",  # Enable flash attention nếu hỗ trợ
        "OLLAMA_HOST": "127.0.0.1:1234"
    }

    print("🔧 Cấu hình environment variables...")
    for key, value in env_vars.items():
        success, _, error = run_command(f'setx {key} "{value}"', capture_output=True)
        if success:
            print(f"  ✅ {key}={value}")
        else:
            print(f"  ⚠️  {key}: {error}")


def preload_model(model_name="llama-3.2-3b-instruct"):
    """Preload model để giảm thời gian load"""
    print(f"\n🚀 Preload model {model_name}...")

    try:
        # Gọi API để load model vào memory
        payload = {
            "model": model_name,
            "prompt": "Hello",
            "stream": False,
            "options": {
                "num_predict": 10
            }
        }

        print("  📦 Đang load model vào memory...")
        response = requests.post(
            "http://127.0.0.1:1234/api/generate",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            print("  ✅ Model đã được load vào memory")
            return True
        else:
            print(f"  ❌ Lỗi load model: {response.status_code}")
            return False

    except Exception as e:
        print(f"  ❌ Lỗi preload: {e}")
        return False


def test_response_time(model_name="llama-3.2-3b-instruct"):
    """Test thời gian phản hồi của model"""
    print(f"\n⏱️ Test thời gian phản hồi...")

    test_prompts = [
        "Xin chào",
        "Gợi ý 1 món ăn ngon",
        "Nhà hàng nào tốt ở Sài Gòn?"
    ]

    total_time = 0
    successful_tests = 0

    for i, prompt in enumerate(test_prompts, 1):
        try:
            print(f"  Test {i}/3: {prompt[:30]}...")

            start_time = time.time()

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 100,
                    "num_predict": 100
                }
            }

            response = requests.post(
                "http://127.0.0.1:1234/api/generate",
                json=payload,
                timeout=30
            )

            end_time = time.time()
            response_time = end_time - start_time

            if response.status_code == 200:
                total_time += response_time
                successful_tests += 1
                print(f"    ✅ {response_time:.2f}s")
            else:
                print(f"    ❌ Lỗi: {response.status_code}")

        except Exception as e:
            print(f"    ❌ Timeout/Error: {e}")

    if successful_tests > 0:
        avg_time = total_time / successful_tests
        print(f"\n📊 Kết quả test:")
        print(f"  • Successful: {successful_tests}/{len(test_prompts)}")
        print(f"  • Avg time: {avg_time:.2f}s")

        if avg_time < 10:
            print("  🎉 Performance tốt!")
        elif avg_time < 20:
            print("  👍 Performance khá ổn")
        else:
            print("  ⚠️  Performance chậm, cần tối ưu thêm")

        return avg_time
    else:
        print("  ❌ Tất cả tests failed")
        return None


def optimize_model_parameters():
    """Đưa ra gợi ý tối ưu parameters"""
    print("\n💡 GỢI Ý TỐI ỨU PERFORMANCE:")
    print("=" * 50)

    print("🔧 Trong code Python (llm_service.py):")
    print("""
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500,        # Giảm từ 1000 → 500
        "num_predict": 500,       # Ollama specific
        "repeat_penalty": 1.1,
        "top_k": 40,
        "stop": ["Human:", "\\n\\n"]  # Stop tokens để dừng sớm
    }
    """)

    print("\n🚀 Trong terminal để khởi động Ollama:")
    print("ollama serve --host 127.0.0.1:1234")

    print("\n⚡ Model alternatives nhanh hơn:")
    print("• ollama pull qwen2:1.5b      # Model 1.5B nhỏ hơn")
    print("• ollama pull phi3:mini       # Microsoft Phi-3 Mini")
    print("• ollama pull gemma:2b        # Google Gemma 2B")

    print("\n🔥 Hardware optimization:")
    print("• Đóng các app không cần thiết")
    print("• Tăng RAM nếu có thể (8GB+ recommended)")
    print("• SSD sẽ load model nhanh hơn HDD")


def main():
    print("🚀 OLLAMA OPTIMIZATION TOOL")
    print("=" * 40)

    # 1. Check Ollama status
    running, models = check_ollama_status()
    if not running:
        print("\n💡 Hãy start Ollama trước:")
        print("ollama serve")
        return

    # 2. Show available models
    print(f"\n📋 Available models:")
    for model in models:
        name = model.get("name", "Unknown")
        size = model.get("size", 0)
        size_mb = size / (1024 * 1024) if size > 0 else 0
        print(f"  • {name} ({size_mb:.0f}MB)")

    # 3. Find best model
    target_models = ["llama3.2:3b", "llama3.2", "qwen2:1.5b", "phi3:mini"]
    selected_model = None

    for target in target_models:
        for model in models:
            if target in model.get("name", ""):
                selected_model = model.get("name")
                break
        if selected_model:
            break

    if not selected_model:
        print("\n❌ Không tìm thấy model phù hợp!")
        print("💡 Hãy pull model:")
        print("ollama pull llama-3.2-3b-instruct")
        return

    print(f"\n🎯 Sử dụng model: {selected_model}")

    # 4. Optimize config
    optimize_ollama_config()

    # 5. Preload model
    preload_model(selected_model)

    # 6. Test performance
    avg_time = test_response_time(selected_model)

    # 7. Show optimization tips
    optimize_model_parameters()

    print(f"\n🎉 OPTIMIZATION COMPLETE!")
    if avg_time and avg_time < 15:
        print("✅ AI response time đã được tối ưu!")
    else:
        print("⚠️  Có thể cần tối ưu thêm - xem gợi ý ở trên")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Đã hủy optimization")
    except Exception as e:
        print(f"\n💥 Lỗi: {e}")
        sys.exit(1)