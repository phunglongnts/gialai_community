import json
import asyncio
import re
from typing import Dict, List, Any, Optional
import httpx
import logging
import os

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        # Ollama native: KHÔNG có /v1
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        # Ollama không yêu cầu API key
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=60.0
        )

        # System prompts
        self.search_system_prompt = """
        Bạn là một AI chuyên gia về ẩm thực và nhà hàng tại Việt Nam. 
        Nhiệm vụ của bạn là giúp khách hàng tìm kiếm và lựa chọn nhà hàng phù hợp.

        Quy tắc trả lời:
        1. Luôn trả lời bằng tiếng Việt
        2. Phân tích yêu cầu của khách hàng một cách chi tiết
        3. Đưa ra gợi ý cụ thể dựa trên database nhà hàng
        4. Giải thích lý do tại sao gợi ý những nhà hàng đó
        5. Đưa ra thông tin hữu ích như giá cả, món ăn đặc trưng, không khí

        Format trả lời:
        - Phần phân tích: Hiểu rõ yêu cầu của khách
        - Phần gợi ý: Top 3-5 nhà hàng phù hợp nhất
        - Phần lý do: Tại sao những nhà hàng này phù hợp
        - Phần bonus: Tips thêm cho khách hàng
        """

        self.chat_system_prompt = """
        Bạn là một trợ lý AI thân thiện chuyên về ẩm thực và nhà hàng.
        Hãy trò chuyện một cách tự nhiên và hữu ích với khách hàng.
        Luôn trả lời bằng tiếng Việt và tập trung vào chủ đề ẩm thực, nhà hàng.
        """

    async def health_check(self) -> str:
        """Kiểm tra trạng thái Ollama và chọn model phù hợp (GET /api/tags)."""
        try:
            r = await self.client.get("/api/tags")
            if r.status_code != 200:
                return f"Ollama not responding: {r.status_code}"

            data = r.json()
            # Ollama trả dạng: {"models":[{"name":"llama3.2:3b-instruct", ...}, ...]}
            models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]

            variations = [
                self.model_name,
                "llama3.2:3b-instruct",
                "llama3.2:latest",
                "llama3.2",
                "llama3"
            ]

            found = None
            for v in variations:
                for avail in models:
                    # Khớp theo chứa chuỗi hoặc theo prefix trước dấu :
                    if v in avail or avail.startswith(v.split(":")[0]):
                        found = avail
                        break
                if found:
                    break

            if found:
                self.model_name = found
                return "OK"
            return f"No compatible Llama model found. Available: {models}"
        except Exception as e:
            return f"ERROR: {str(e)} - Please ensure Ollama is running on {self.base_url}"

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Gọi Ollama native để sinh phản hồi (POST /api/generate)."""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                # Ollama hỗ trợ 'system' để set system prompt
                "system": system_prompt or "",
                # Tùy chọn sampling (Ollama: temperature, top_p, num_predict = max_tokens)
                "options": {
                    "temperature": 0.5,     # Giảm creativity để nhanh hơn
                    "top_p": 0.8,          # Giảm từ 0.9
                    "max_tokens": 400,     # Giảm thêm nếu muốn
                    "repeat_penalty": 1.1,
                    "stop": ["Human:", "User:", "\n\n"]  # Stop sớm
                }
            }

            r = await self.client.post("/api/generate", json=payload)
            if r.status_code == 200:
                # Với stream=False, Ollama trả một JSON duy nhất có key "response"
                # (hoặc có thể trả thêm các trường done, eval_count...)
                j = r.json()
                return j.get("response", "Xin lỗi, tôi không thể trả lời lúc này.")
            else:
                logger.error(f"LLM API error: {r.status_code} {r.text}")
                return "Xin lỗi, có lỗi xảy ra với hệ thống AI."
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return "Xin lỗi, tôi không thể trả lời lúc này. Vui lòng thử lại."

    # -------------------- Business logic giữ nguyên --------------------

    def create_restaurant_context(self, restaurants: List[Dict]) -> str:
        context = "DANH SÁCH NHÀ HÀNG HIỆN CÓ:\n\n"
        for i, restaurant in enumerate(restaurants, 1):
            context += f"{i}. {restaurant['name']}\n"
            context += f"   - Loại: {restaurant.get('category', 'N/A')}\n"
            context += f"   - Địa chỉ: {restaurant.get('address', 'N/A')}\n"
            context += f"   - Mô tả: {restaurant.get('description', 'N/A')}\n"
            context += f"   - Giá: {restaurant.get('price_range', 'N/A')}\n"
            context += f"   - Đánh giá: {restaurant.get('average_rating', 0)}/5 ({restaurant.get('total_reviews', 0)} đánh giá)\n"

            features = restaurant.get('features', [])
            if features:
                context += f"   - Tiện ích: {', '.join(features)}\n"

            cuisines = restaurant.get('cuisine_types', [])
            if cuisines:
                context += f"   - Món ăn: {', '.join(cuisines)}\n"

            context += "\n"
        return context

    async def search_restaurants(self, query: str, restaurant_context: str) -> Dict[str, Any]:
        try:
            search_prompt = f"""
{restaurant_context}

YÊU CẦU CỦA KHÁCH HÀNG: "{query}"

Hãy phân tích yêu cầu và đưa ra gợi ý nhà hàng phù hợp nhất.
Trả lời theo format sau:

**PHÂN TÍCH YÊU CẦU:**
[Phân tích ngắn gọn về yêu cầu của khách hàng]

**GỢI Ý NHÀ HÀNG:**
[Danh sách 3-5 nhà hàng phù hợp nhất với lý do]

**KHUYẾN NGHỊ:**
[Tips và lời khuyên thêm cho khách hàng]
"""
            ai_response = await self.generate_response(search_prompt, self.search_system_prompt)
            recommended_ids = self.extract_restaurant_recommendations(ai_response, restaurant_context)
            return {
                "response": ai_response,
                "recommendations": recommended_ids,
                "confidence_score": 0.8
            }
        except Exception as e:
            logger.error(f"Search restaurants error: {str(e)}")
            return {
                "response": "Xin lỗi, có lỗi xảy ra khi tìm kiếm. Vui lòng thử lại.",
                "recommendations": [],
                "confidence_score": 0.0
            }

    def extract_restaurant_recommendations(self, ai_response: str, context: str) -> List[int]:
        recommended_ids = []
        restaurant_map = {}
        for line in context.split('\n'):
            if '. ' in line and line.strip():
                parts = line.split('. ')
                if len(parts) >= 2:
                    try:
                        idx = int(parts[0])
                        name = parts[1].strip()
                        restaurant_map[name.lower()] = idx
                    except ValueError:
                        continue

        ai_response_lower = ai_response.lower()
        for name, idx in restaurant_map.items():
            if name in ai_response_lower:
                recommended_ids.append(idx)

        return recommended_ids[:5]

    async def chat_with_context(self, message: str, context: str, history: List[Dict[str, str]] = None) -> str:
        try:
            history_str = ""
            if history:
                for msg in history[-5:]:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    history_str += f"{role.upper()}: {content}\n"

            history_section = f"LỊCH SỬ HỘI THOẠI:\n{history_str}" if history_str else ""

            chat_prompt = f"""
CONTEXT VỀ NHÀ HÀNG:
{context[:2000]}

{history_section}

KHÁCH HÀNG: {message}

Hãy trả lời một cách tự nhiên và hữu ích. Nếu khách hàng hỏi về nhà hàng cụ thể, 
hãy sử dụng thông tin từ context để trả lời chính xác.
"""
            return await self.generate_response(chat_prompt, self.chat_system_prompt)
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return "Xin lỗi, tôi không thể trả lời lúc này. Vui lòng thử lại."

    async def analyze_review_sentiment(self, review_text: str) -> Dict[str, Any]:
        try:
            prompt = f"""
Phân tích đánh giá sau về nhà hàng và cho biết:
1. Sentiment tổng thể (tích cực/tiêu cực/trung tính)
2. Điểm mạnh được nhắc đến
3. Điểm yếu được nhắc đến
4. Đánh giá về từng khía cạnh: món ăn, phục vụ, không gian, giá cả

ĐÁNH GIÁ: "{review_text}"

Trả lời ngắn gọn bằng tiếng Việt theo format JSON:
{{
    "sentiment": "positive/negative/neutral",
    "strengths": ["điểm mạnh 1", "điểm mạnh 2"],
    "weaknesses": ["điểm yếu 1", "điểm yếu 2"],
    "food_score": 4,
    "service_score": 3,
    "ambiance_score": 4,
    "value_score": 3,
    "summary": "Tóm tắt ngắn gọn"
}}
"""
            response = await self.generate_response(prompt)

            # Cố gắng parse JSON từ output LLM
            try:
                m = re.search(r'\{.*\}', response, re.DOTALL)
                if m:
                    return json.loads(m.group())
            except json.JSONDecodeError:
                pass

            # Fallback heuristic
            t = review_text.lower()
            sentiment = "neutral"
            if any(w in t for w in ["tốt", "ngon", "tuyệt", "hài lòng", "thích"]):
                sentiment = "positive"
            elif any(w in t for w in ["tệ", "dở", "không ngon", "thất vọng"]):
                sentiment = "negative"

            return {
                "sentiment": sentiment,
                "strengths": [],
                "weaknesses": [],
                "food_score": 3,
                "service_score": 3,
                "ambiance_score": 3,
                "value_score": 3,
                "summary": "Phân tích cơ bản"
            }
        except Exception as e:
            logger.error(f"Review analysis error: {str(e)}")
            return {
                "sentiment": "neutral",
                "strengths": [],
                "weaknesses": [],
                "food_score": 3,
                "service_score": 3,
                "ambiance_score": 3,
                "value_score": 3,
                "summary": "Không thể phân tích"
            }

    async def generate_restaurant_description(self, restaurant_info: Dict[str, Any]) -> str:
        try:
            features_text = ', '.join(restaurant_info.get('features', []))
            cuisines_text = ', '.join(restaurant_info.get('cuisine_types', []))
            prompt = f"""
Tạo mô tả hấp dẫn (2-3 câu) cho nhà hàng:

Tên: {restaurant_info.get('name', '')}
Loại: {restaurant_info.get('category', '')}
Địa chỉ: {restaurant_info.get('address', '')}
Giá cả: {restaurant_info.get('price_range', '')}
Tiện ích: {features_text}
Món ăn: {cuisines_text}
"""
            return await self.generate_response(prompt)
        except Exception as e:
            logger.error(f"Description generation error: {str(e)}")
            return "Nhà hàng chất lượng với phong cách phục vụ tận tâm."

    async def suggest_menu_items(self, restaurant_context: str, user_preferences: str) -> List[str]:
        try:
            prompt = f"""
Dựa trên thông tin nhà hàng và sở thích của khách hàng, 
hãy gợi ý 3-5 món ăn phù hợp nhất.

THÔNG TIN NHÀ HÀNG:
{restaurant_context}

SỞ THÍCH KHÁCH HÀNG: {user_preferences}

Trả lời danh sách món ăn, mỗi món một dòng với format:
- Tên món: Mô tả ngắn
"""
            response = await self.generate_response(prompt)
            items = []
            for line in response.split('\n'):
                s = line.strip()
                if s.startswith('-') or s.startswith('•'):
                    items.append(s.lstrip('-•').strip())
            return items[:5] or ["Món đặc sản của nhà hàng", "Món phổ biến nhất", "Món theo mùa"]
        except Exception as e:
            logger.error(f"Menu suggestion error: {str(e)}")
            return ["Món đặc sản của nhà hàng", "Món phổ biến nhất", "Món theo mùa"]

    async def close(self):
        """Đóng kết nối HTTPX."""
        await self.client.aclose()
