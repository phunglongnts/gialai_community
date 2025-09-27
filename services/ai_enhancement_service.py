import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

from services.llm_service import LLMService
from schemas import RestaurantCreateRequest, AIEnhancementResponse
from utils.text_utils import clean_text, extract_keywords


class RestaurantAIEnhancementService:
    """Service để AI cải thiện thông tin nhà hàng"""

    def __init__(self):
        self.llm = LLMService()
        self.enhancement_prompts = self._load_enhancement_prompts()

    def _load_enhancement_prompts(self) -> Dict[str, str]:
        """Load các template prompt cho từng loại enhancement"""
        return {
            "description": """
Bạn là chuyên gia marketing nhà hàng tại Việt Nam. 
Nhiệm vụ: Viết lại mô tả nhà hàng hấp dẫn, chuyên nghiệp và thu hút khách hàng.

THÔNG TIN NHÀ HÀNG:
- Tên: {name}
- Loại ẩm thực: {cuisine_type}
- Mô tả gốc: {description}
- Địa chỉ: {address}
- Mức giá: {price_range}
- Tiện ích: {facilities}

YÊU CẦU:
1. Viết mô tả dài 150-200 từ
2. Tôn vinh điểm mạnh của nhà hàng
3. Sử dụng ngôn từ Việt Nam, gần gũi
4. Nhấn mạnh trải nghiệm khách hàng
5. Kết thúc bằng lời mời gọi hành động

PHONG CÁCH: Thân thiện, chuyên nghiệp, không quá phô trương.
            """,

            "menu_suggestions": """
Bạn là đầu bếp chuyên nghiệp am hiểu ẩm thực {cuisine_type}.
Nhiệm vụ: Đề xuất menu đa dạng, hấp dẫn cho nhà hàng.

THÔNG TIN NHÀ HÀNG:
- Tên: {name}
- Loại ẩm thực: {cuisine_type}  
- Mức giá: {price_range}
- Mô tả: {description}

YÊU CẦU MENU:
1. 15-20 món ăn đa dạng
2. Phân loại: Khai vị, Món chính, Tráng miệng, Nước uống
3. Mỗi món có: Tên món, Mô tả ngắn (20-30 từ), Giá ước tính
4. Phù hợp với mức giá {price_range}
5. Có 3-5 món đặc sản nổi bật

FORMAT TRUYỀN DỀN:
**KHAI VỊ**
- Tên món (Giá): Mô tả hấp dẫn

**MÓN CHÍNH**  
- Tên món (Giá): Mô tả hấp dẫn

**TRÁNG MIỆNG**
- Tên món (Giá): Mô tả hấp dẫn

**NƯỚC UỐNG**
- Tên món (Giá): Mô tả hấp dẫn

🌟 **MÓN ĐẶC SAN KHÔNG THỂ BỎ LỠ:**
- Liệt kê 3-5 món signature với lý do nên thử
            """,

            "seo_content": """
Bạn là chuyên gia SEO cho nhà hàng tại Việt Nam.
Nhiệm vụ: Tạo nội dung SEO để nhà hàng xuất hiện cao trong tìm kiếm.

THÔNG TIN NHÀ HÀNG:
- Tên: {name}
- Loại ẩm thực: {cuisine_type}
- Địa chỉ: {address}
- Mô tả: {description}

TẠO NỘI DUNG SEO:

1. **Title Tag** (50-60 ký tự):
   - Chứa tên nhà hàng + loại ẩm thực + địa điểm

2. **Meta Description** (150-160 ký tự):
   - Mô tả hấp dẫn, có call-to-action

3. **Keywords chính** (10-15 từ khóa):
   - Từ khóa liên quan đến món ăn, địa điểm

4. **Long-tail keywords** (5-10 cụm từ dài):
   - Câu hỏi khách hàng thường tìm

5. **Hashtags** (10-15 hashtags):
   - Cho social media

FORMAT TRUYỂN VỀ JSON:
{{
    "title": "...",
    "meta_description": "...",
    "primary_keywords": [...],
    "long_tail_keywords": [...], 
    "hashtags": [...],
    "content_topics": [...]
}}
            """,

            "social_content": """
Bạn là content creator chuyên nghiệp cho nhà hàng.
Nhiệm vụ: Tạo nội dung mạng xã hội thu hút khách hàng.

THÔNG TIN NHÀ HÀNG:
- Tên: {name}
- Loại ẩm thực: {cuisine_type}
- Mô tả: {description}
- Điểm mạnh: {facilities}

TẠO CONTENT:

1. **Facebook Post** (2-3 posts khác nhau):
   - Post giới thiệu nhà hàng
   - Post về món ăn đặc sắc
   - Post về trải nghiệm khách hàng

2. **Instagram Captions** (3 captions):
   - Foodie style với emoji
   - Story style casual
   - Professional introduction

3. **Google My Business Posts** (2 posts):
   - Grand opening announcement
   - Special dish highlight

Sử dụng emojis, hashtags phù hợp. Ngôn ngữ thân thiện, gần gũi với người Việt.
            """
        }

    async def enhance_restaurant_info(
            self,
            restaurant_data: RestaurantCreateRequest
    ) -> AIEnhancementResponse:
        """Main function để AI enhancement toàn bộ thông tin nhà hàng"""

        start_time = datetime.now()

        try:
            # Chạy song song các task enhancement
            tasks = []

            if restaurant_data.enable_ai_enhancement:
                tasks.extend([
                    self._enhance_description(restaurant_data),
                    self._generate_menu_suggestions(restaurant_data),
                    self._create_seo_content(restaurant_data)
                ])

            # Đợi tất cả tasks hoàn thành
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Parse results
            enhanced_description = results[0] if len(results) > 0 and not isinstance(results[0], Exception) else None
            menu_suggestions = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else None
            seo_content = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else None

            processing_time = (datetime.now() - start_time).total_seconds()

            return AIEnhancementResponse(
                enhanced_description=enhanced_description,
                menu_suggestions=menu_suggestions,
                seo_content=seo_content,
                processing_time=processing_time
            )

        except Exception as e:
            print(f"Lỗi AI Enhancement: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds()

            return AIEnhancementResponse(
                enhanced_description=None,
                menu_suggestions=None,
                seo_content=None,
                processing_time=processing_time
            )

    async def _enhance_description(self, data: RestaurantCreateRequest) -> Optional[str]:
        """AI cải thiện mô tả nhà hàng"""
        try:
            prompt = self.enhancement_prompts["description"].format(
                name=data.name,
                cuisine_type=data.cuisine_type,
                description=data.description,
                address=data.address,
                price_range=self._translate_price_range(data.price_range),
                facilities=self._format_facilities(data.facilities)
            )

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            print(f"Lỗi enhance description: {str(e)}")
            return None

    async def _generate_menu_suggestions(self, data: RestaurantCreateRequest) -> Optional[str]:
        """AI tạo gợi ý menu"""
        try:
            prompt = self.enhancement_prompts["menu_suggestions"].format(
                name=data.name,
                cuisine_type=data.cuisine_type,
                price_range=self._translate_price_range(data.price_range),
                description=data.description
            )

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            print(f"Lỗi generate menu: {str(e)}")
            return None

    async def _create_seo_content(self, data: RestaurantCreateRequest) -> Optional[Dict[str, Any]]:
        """AI tạo nội dung SEO"""
        try:
            prompt = self.enhancement_prompts["seo_content"].format(
                name=data.name,
                cuisine_type=data.cuisine_type,
                address=data.address,
                description=data.description
            )

            response = await self.llm.generate_response(prompt)

            # Thử parse JSON response
            try:
                seo_data = json.loads(response)
                return seo_data
            except:
                # Nếu không parse được JSON, trả về format đơn giản
                return {
                    "title": f"{data.name} - {data.cuisine_type} {data.address}",
                    "meta_description": data.description[:150] + "...",
                    "keywords": [data.name, data.cuisine_type, data.province]
                }

        except Exception as e:
            print(f"Lỗi create SEO content: {str(e)}")
            return None

    async def generate_social_content(self, data: RestaurantCreateRequest) -> Optional[Dict[str, List[str]]]:
        """AI tạo content cho social media"""
        try:
            prompt = self.enhancement_prompts["social_content"].format(
                name=data.name,
                cuisine_type=data.cuisine_type,
                description=data.description,
                facilities=self._format_facilities(data.facilities)
            )

            response = await self.llm.generate_response(prompt)

            # Parse response thành các loại content
            content_data = self._parse_social_content(response)
            return content_data

        except Exception as e:
            print(f"Lỗi generate social content: {str(e)}")
            return None

    async def suggest_improvements(self, restaurant_data: RestaurantCreateRequest) -> List[str]:
        """AI gợi ý cải thiện thông tin nhà hàng"""
        try:
            suggestions = []

            # Check thông tin thiếu
            if not restaurant_data.logo_url:
                suggestions.append("📷 Thêm logo nhà hàng để tăng tính chuyên nghiệp")

            if not restaurant_data.cover_image_url:
                suggestions.append("🖼️ Thêm ảnh bìa đẹp để thu hút khách hàng")

            if not restaurant_data.gallery_images or len(restaurant_data.gallery_images) < 3:
                suggestions.append("📸 Thêm ít nhất 3-5 ảnh món ăn để showcase menu")

            if not restaurant_data.opening_hours or len(restaurant_data.opening_hours) == 0:
                suggestions.append("🕐 Cập nhật giờ mở cửa chi tiết để khách biết khi nào có thể đến")

            if len(restaurant_data.description) < 50:
                suggestions.append("📝 Mô tả nhà hàng nên dài hơn để khách hiểu rõ về địa điểm")

            if not restaurant_data.facilities or len(restaurant_data.facilities) == 0:
                suggestions.append("✨ Thêm thông tin tiện ích (WiFi, chỗ đỗ xe, điều hòa...) để thu hút khách")

            # AI suggestions based on cuisine type
            cuisine_suggestions = await self._get_cuisine_specific_suggestions(restaurant_data.cuisine_type)
            suggestions.extend(cuisine_suggestions)

            return suggestions[:8]  # Giới hạn 8 suggestions

        except Exception as e:
            print(f"Lỗi suggest improvements: {str(e)}")
            return []

    async def _get_cuisine_specific_suggestions(self, cuisine_type: str) -> List[str]:
        """Gợi ý specific theo loại ẩm thực"""
        suggestions_map = {
            "Việt Nam": [
                "🥢 Highlight các món đặc sản địa phương như phở, bún bò Huế, bánh mì",
                "🌿 Nhấn mạnh về nguyên liệu tươi ngon, cách chế biến truyền thống"
            ],
            "Nhật Bản": [
                "🍣 Showcase sushi bar và tính tươi ngon của hải sản",
                "🎋 Tạo không gian zen, nhấn mạnh văn hóa ẩm thực Nhật"
            ],
            "Hàn Quốc": [
                "🌶️ Highlight các món nướng BBQ và kimchi tự làm",
                "🥘 Nhấn mạnh về banchan (món ăn kèm) đa dạng"
            ],
            "Trung Hoa": [
                "🥟 Showcase dim sum và các món xào đặc sắc",
                "🍜 Nhấn mạnh về nước dùng đậm đà, cook-to-order"
            ]
        }

        return suggestions_map.get(cuisine_type, [
            "🍽️ Tạo signature dishes độc đáo riêng của nhà hàng",
            "⭐ Highlight điểm mạnh về phục vụ và không gian"
        ])

    def _translate_price_range(self, price_range: Optional[str]) -> str:
        """Dịch price range sang tiếng Việt"""
        translation_map = {
            "cheap": "bình dân (dưới 100k/người)",
            "medium": "trung bình (100k-300k/người)",
            "expensive": "cao cấp (trên 300k/người)"
        }
        return translation_map.get(price_range, "trung bình")

    def _format_facilities(self, facilities: Optional[List[str]]) -> str:
        """Format danh sách tiện ích"""
        if not facilities:
            return "Chưa có thông tin tiện ích"

        facility_translation = {
            "wifi": "WiFi miễn phí",
            "parking": "Chỗ đỗ xe",
            "outdoor_seating": "Chỗ ngồi ngoài trời",
            "air_conditioning": "Điều hòa",
            "takeaway": "Mang về",
            "delivery": "Giao hàng"
        }

        translated = [facility_translation.get(f, f) for f in facilities]
        return ", ".join(translated)

    def _parse_social_content(self, response: str) -> Dict[str, List[str]]:
        """Parse response thành social content structure"""
        try:
            content_data = {
                "facebook_posts": [],
                "instagram_captions": [],
                "google_posts": []
            }

            # Simple parsing logic - có thể cải thiện sau
            sections = response.split("**")
            current_section = ""

            for section in sections:
                if "Facebook Post" in section:
                    current_section = "facebook_posts"
                elif "Instagram" in section:
                    current_section = "instagram_captions"
                elif "Google" in section:
                    current_section = "google_posts"
                elif current_section and section.strip():
                    # Clean up and add to appropriate section
                    clean_content = clean_text(section)
                    if clean_content:
                        content_data[current_section].append(clean_content)

            return content_data

        except Exception as e:
            print(f"Lỗi parse social content: {str(e)}")
            return {
                "facebook_posts": ["Content parsing error"],
                "instagram_captions": ["Content parsing error"],
                "google_posts": ["Content parsing error"]
            }


# ================================
# Utility functions
# ================================

class RestaurantImageAnalyzer:
    """Analyzer để phân tích ảnh và gợi ý mô tả"""

    def __init__(self):
        self.llm = LLMService()

    async def analyze_food_images(self, image_urls: List[str]) -> List[Dict[str, str]]:
        """Phân tích ảnh món ăn và tạo mô tả"""
        # Placeholder - sẽ implement computer vision sau
        # Hiện tại return mock data

        suggestions = []
        for i, url in enumerate(image_urls[:5]):  # Giới hạn 5 ảnh
            suggestions.append({
                "image_url": url,
                "suggested_description": f"Món ăn số {i + 1} - Trông hấp dẫn và ngon miệng",
                "estimated_category": "Món chính",
                "suggested_price_range": "100k-200k"
            })

        return suggestions

    async def generate_alt_text(self, image_url: str, context: str = "") -> str:
        """Tạo alt text cho ảnh (SEO)"""
        # Placeholder implementation
        return f"Ảnh món ăn tại nhà hàng - {context}"


# ================================
# Review Analysis Service
# ================================

class ReviewAnalysisService:
    """Service để phân tích đánh giá bằng AI"""

    def __init__(self):
        self.llm = LLMService()

    async def analyze_review_sentiment(self, review_content: str) -> Dict[str, Any]:
        """Phân tích sentiment của review"""
        try:
            prompt = f"""
Phân tích sentiment của đánh giá nhà hàng sau:

ĐÁNH GIÁ: "{review_content}"

Trả về kết quả JSON với format:
{{
    "sentiment_score": số từ -1.0 đến 1.0,
    "sentiment_label": "positive/negative/neutral",
    "key_points": ["điểm mạnh 1", "điểm mạnh 2", ...],
    "concerns": ["vấn đề 1", "vấn đề 2", ...],
    "summary": "Tóm tắt ngắn gọn đánh giá"
}}
"""

            response = await self.llm.generate_response(prompt)

            try:
                return json.loads(response)
            except:
                # Fallback nếu không parse được JSON
                return {
                    "sentiment_score": 0.0,
                    "sentiment_label": "neutral",
                    "key_points": [],
                    "concerns": [],
                    "summary": review_content[:100] + "..."
                }

        except Exception as e:
            print(f"Lỗi analyze sentiment: {str(e)}")
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "key_points": [],
                "concerns": [],
                "summary": "Không thể phân tích"
            }

    async def suggest_owner_response(self, review_content: str, restaurant_name: str) -> str:
        """AI gợi ý phản hồi cho chủ nhà hàng"""
        try:
            prompt = f"""
Bạn là chủ nhà hàng "{restaurant_name}". Một khách hàng vừa để lại đánh giá:

ĐÁNH GIÁ: "{review_content}"

Hãy viết một phản hồi chuyên nghiệp, thân thiện:

YÊU CẦU:
1. Cảm ơn khách hàng
2. Thừa nhận góp ý (nếu có vấn đề)  
3. Cam kết cải thiện (nếu cần)
4. Mời khách quay lại
5. Dài khoảng 50-80 từ
6. Tone thân thiện, chân thành

PHẢN HỒI:
"""

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            print(f"Lỗi suggest owner response: {str(e)}")
            return f"Cảm ơn bạn đã đánh giá {restaurant_name}! Chúng tôi rất trân trọng góp ý và sẽ không ngừng cải thiện để phục vụ bạn tốt hơn."

    async def extract_review_insights(self, reviews: List[str]) -> Dict[str, Any]:
        """Phân tích tổng quan từ nhiều reviews"""
        try:
            if not reviews:
                return {"insights": "Chưa có đánh giá nào"}

            # Combine reviews với limit length
            combined_reviews = "\n".join(reviews[:20])  # Giới hạn 20 reviews
            if len(combined_reviews) > 3000:
                combined_reviews = combined_reviews[:3000] + "..."

            prompt = f"""
Phân tích tổng quan từ các đánh giá nhà hàng sau:

CÁC ĐÁNH GIÁ:
{combined_reviews}

Trả về phân tích JSON:
{{
    "overall_sentiment": "positive/negative/mixed",
    "strengths": ["điểm mạnh 1", "điểm mạnh 2", ...],
    "weaknesses": ["điểm yếu 1", "điểm yếu 2", ...],
    "common_compliments": ["khen ngợi thường thấy"],
    "common_complaints": ["khiếu nại thường thấy"],
    "improvement_suggestions": ["gợi ý cải thiện 1", "gợi ý 2", ...],
    "summary": "Tóm tắt tổng quan 2-3 câu"
}}
"""

            response = await self.llm.generate_response(prompt)

            try:
                return json.loads(response)
            except:
                return {"insights": "Không thể phân tích reviews"}

        except Exception as e:
            print(f"Lỗi extract review insights: {str(e)}")
            return {"insights": f"Lỗi phân tích: {str(e)}"}


# ================================
# Smart Search Service
# ================================

class SmartSearchService:
    """Service cho AI search thông minh"""

    def __init__(self):
        self.llm = LLMService()

    async def interpret_search_query(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """AI hiểu và phân tích câu hỏi tìm kiếm"""
        try:
            context_info = ""
            if user_context:
                location = user_context.get("location", "")
                if location:
                    context_info = f"Vị trí người dùng: {location}\n"

            prompt = f"""
Phân tích câu hỏi tìm kiếm nhà hàng của người dùng:

{context_info}
CÂU HỎI: "{query}"

Trả về JSON với thông tin:
{{
    "intent": "find_restaurant/compare_restaurants/get_recommendation/ask_about_food",
    "cuisine_preferences": ["loại ẩm thực được nhắc"],
    "price_preferences": "cheap/medium/expensive hoặc null",
    "location_preferences": ["địa điểm được nhắc"],
    "occasion": "date/family/business/casual hoặc null",
    "dietary_requirements": ["chay/halal/không cay/etc"],
    "facilities_needed": ["wifi/parking/outdoor/etc"],
    "keywords": ["từ khóa quan trọng"],
    "search_filters": {{
        "cuisine_type": "...",
        "price_range": "...",
        "facilities": [...],
        "location": "..."
    }},
    "natural_response": "Câu trả lời tự nhiên cho người dùng"
}}
"""

            response = await self.llm.generate_response(prompt)

            try:
                return json.loads(response)
            except:
                # Fallback parsing
                return {
                    "intent": "find_restaurant",
                    "keywords": [query],
                    "natural_response": f"Tôi hiểu bạn đang tìm kiếm: {query}"
                }

        except Exception as e:
            print(f"Lỗi interpret search query: {str(e)}")
            return {
                "intent": "find_restaurant",
                "keywords": [query],
                "natural_response": "Xin lỗi, tôi không hiểu rõ yêu cầu của bạn."
            }

    async def generate_search_explanation(
            self,
            query: str,
            restaurants: List[Dict],
            search_criteria: Dict
    ) -> str:
        """AI giải thích tại sao gợi ý những nhà hàng này"""
        try:
            restaurant_names = [r.get("name", "Nhà hàng") for r in restaurants[:5]]

            prompt = f"""
Người dùng tìm kiếm: "{query}"

Hệ thống đã tìm thấy các nhà hàng: {", ".join(restaurant_names)}

Tiêu chí tìm kiếm: {search_criteria}

Hãy viết một đoạn giải thích 2-3 câu tại sao gợi ý những nhà hàng này.
Tone thân thiện, tự nhiên như một người bạn đang tư vấn.

GIẢI THÍCH:
"""

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            print(f"Lỗi generate search explanation: {str(e)}")
            return "Đây là những nhà hàng phù hợp với yêu cầu của bạn."

    async def generate_additional_tips(self, query: str, context: Dict = None) -> Optional[str]:
        """AI tạo tips thêm cho người dùng"""
        try:
            prompt = f"""
Người dùng vừa tìm kiếm: "{query}"

Hãy đưa ra 1-2 lời khuyên hữu ích liên quan đến:
- Thời gian tốt nhất để đến nhà hàng
- Món nên thử
- Cách đặt bàn
- Lưu ý đặc biệt

Viết ngắn gọn, thân thiện, thực tế.

TIPS:
"""

            response = await self.llm.generate_response(prompt)
            tips = clean_text(response)

            return tips if len(tips) > 20 else None

        except Exception as e:
            print(f"Lỗi generate additional tips: {str(e)}")
            return None


# ================================
# Content Optimization Service
# ================================

class ContentOptimizationService:
    """Service tối ưu hóa nội dung"""

    def __init__(self):
        self.llm = LLMService()

    async def optimize_restaurant_content(self, restaurant_data: Dict[str, Any]) -> Dict[str, str]:
        """Tối ưu hóa toàn bộ nội dung nhà hàng"""
        optimizations = {}

        try:
            # Optimize description
            if restaurant_data.get("description"):
                optimizations["description"] = await self._optimize_description(
                    restaurant_data["description"],
                    restaurant_data.get("cuisine_type"),
                    restaurant_data.get("name")
                )

            # Optimize menu items
            if restaurant_data.get("menu_items"):
                optimizations["menu_descriptions"] = await self._optimize_menu_items(
                    restaurant_data["menu_items"]
                )

            return optimizations

        except Exception as e:
            print(f"Lỗi optimize content: {str(e)}")
            return {}

    async def _optimize_description(self, description: str, cuisine_type: str, restaurant_name: str) -> str:
        """Tối ưu hóa mô tả nhà hàng"""
        try:
            prompt = f"""
Tối ưu hóa mô tả nhà hàng cho SEO và user experience:

TÊN NHÀ HÀNG: {restaurant_name}
LOẠI ẨM THỰC: {cuisine_type}
MÔ TẢ HIỆN TẠI: {description}

YÊU CẦU:
1. Giữ ý nghĩa gốc
2. Thêm keywords tự nhiên
3. Cải thiện readability
4. Tăng tính hấp dẫn
5. Độ dài 150-200 từ

MÔ TẢ TỐI ƯU:
"""

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            print(f"Lỗi optimize description: {str(e)}")
            return description

    async def _optimize_menu_items(self, menu_items: List[Dict]) -> List[Dict]:
        """Tối ưu hóa mô tả các món ăn"""
        optimized_items = []

        for item in menu_items[:10]:  # Giới hạn 10 items
            try:
                if item.get("description"):
                    optimized_desc = await self._optimize_single_menu_item(
                        item["name"],
                        item["description"]
                    )

                    optimized_items.append({
                        "id": item.get("id"),
                        "name": item["name"],
                        "original_description": item["description"],
                        "optimized_description": optimized_desc
                    })
            except:
                continue

        return optimized_items

    async def _optimize_single_menu_item(self, item_name: str, description: str) -> str:
        """Tối ưu hóa mô tả một món ăn"""
        try:
            prompt = f"""
Tối ưu hóa mô tả món ăn:

TÊN MÓN: {item_name}
MÔ TẢ HIỆN TẠI: {description}

YÊU CẦU:
1. Làm cho hấp dẫn hơn
2. Thêm chi tiết về hương vị, texture
3. Tối đa 30-40 từ
4. Giữ tính chính xác

MÔ TẢ MỚI:
"""

            response = await self.llm.generate_response(prompt)
            return clean_text(response)

        except Exception as e:
            return description


# ================================
# Recommendation Engine
# ================================

class RestaurantRecommendationEngine:
    """Engine gợi ý nhà hàng thông minh"""

    def __init__(self):
        self.llm = LLMService()

    async def get_personalized_recommendations(
            self,
            user_preferences: Dict[str, Any],
            user_history: List[Dict] = None,
            context: Dict[str, Any] = None
    ) -> List[Dict]:
        """Gợi ý nhà hàng dựa trên preferences và lịch sử"""

        try:
            # Build context cho AI
            context_prompt = self._build_recommendation_context(
                user_preferences,
                user_history,
                context
            )

            # Get recommendations from AI
            recommendations = await self._generate_ai_recommendations(context_prompt)

            return recommendations

        except Exception as e:
            print(f"Lỗi get recommendations: {str(e)}")
            return []

    def _build_recommendation_context(
            self,
            preferences: Dict,
            history: List[Dict],
            context: Dict
    ) -> str:
        """Build context string cho AI recommendations"""

        context_parts = []

        # User preferences
        if preferences:
            prefs = []
            if preferences.get("cuisine_types"):
                prefs.append(f"Ẩm thực yêu thích: {', '.join(preferences['cuisine_types'])}")
            if preferences.get("price_range"):
                prefs.append(f"Mức giá: {preferences['price_range']}")
            if preferences.get("dietary_restrictions"):
                prefs.append(f"Hạn chế ăn uống: {', '.join(preferences['dietary_restrictions'])}")

            if prefs:
                context_parts.append("SỞ THÍCH:\n" + "\n".join(prefs))

        # User history
        if history:
            recent_visits = history[-5:]  # 5 lần gần nhất
            history_text = []
            for visit in recent_visits:
                rating = visit.get("rating", "N/A")
                restaurant = visit.get("restaurant_name", "Unknown")
                history_text.append(f"- {restaurant} (đánh giá: {rating}/5)")

            context_parts.append("LỊCH SỬ GẦN ĐÂY:\n" + "\n".join(history_text))

        # Current context
        if context:
            context_info = []
            if context.get("occasion"):
                context_info.append(f"Dịp: {context['occasion']}")
            if context.get("group_size"):
                context_info.append(f"Số người: {context['group_size']}")
            if context.get("time"):
                context_info.append(f"Thời gian: {context['time']}")

            if context_info:
                context_parts.append("NGỮ CẢNH HIỆN TẠI:\n" + "\n".join(context_info))

        return "\n\n".join(context_parts)

    async def _generate_ai_recommendations(self, context: str) -> List[Dict]:
        """AI tạo recommendations"""
        try:
            prompt = f"""
Dựa trên thông tin người dùng sau, hãy gợi ý 5 nhà hàng phù hợp:

{context}

Trả về JSON array với format:
[
    {{
        "restaurant_name": "Tên nhà hàng",
        "cuisine_type": "Loại ẩm thực", 
        "reason": "Lý do gợi ý (1-2 câu)",
        "recommended_dishes": ["món 1", "món 2"],
        "price_estimate": "100k-200k/người",
        "match_score": 85
    }}
]
"""

            response = await self.llm.generate_response(prompt)

            try:
                return json.loads(response)
            except:
                return []

        except Exception as e:
            print(f"Lỗi generate AI recommendations: {str(e)}")
            return []