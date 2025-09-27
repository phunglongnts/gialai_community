// Step Components
  const Step1 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Thông tin cơ bản về nhà hàng</h2>
        <p className="text-gray-600">Hãy cho chúng tôi biết về nhà hàng của bạn</p>
      </div>

      <div className="space-y-6">
        {/* Restaurant Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tên nhà hàng *
            <span className="text-xs text-gray-500 ml-2">(Tên này sẽ hiển thị công khai)</span>
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            className={`
              w-full px-4 py-3 border rounded-lg text-lg font-medium focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors
              ${errors.name ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:bg-white'}
            `}
            placeholder="VD: Nhà hàng Hương Việt, Quán Phở Sài Gòn, Sushi Ichiban..."
            maxLength={100}
          />
          <div className="flex justify-between items-center mt-1">
            {errors.name && <p className="text-sm text-red-600">{errors.name}</p>}
            <p className="text-xs text-gray-500 ml-auto">{formData.name.length}/100</p>
          </div>
        </div>

        {/* Cuisine Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Loại ẩm thực *
            <span className="text-xs text-gray-500 ml-2">(Chọn loại phù hợp nhất)</span>
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {cuisineTypes.map(type => (
              <div
                key={type.value}
                onClick={() => handleInputChange('cuisine_type', type.value)}
                className={`
                  p-4 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md
                  ${formData.cuisine_type === type.value 
                    ? 'border-blue-500 bg-blue-50 shadow-md' 
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">{type.emoji}</div>
                  <div className="text-sm font-medium text-gray-900">{type.label}</div>
                </div>
              </div>
            ))}
          </div>
          {errors.cuisine_type && <p className="mt-2 text-sm text-red-600">{errors.cuisine_type}</p>}
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mô tả về nhà hàng *
            <span className="text-xs text-gray-500 ml-2">(AI sẽ giúp cải thiện mô tả này)</span>
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            rows={4}
            className={`
              w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors resize-none
              ${errors.description ? 'border-red-500 bg-red-50' : 'border-gray-300 focus:bg-white'}
            `}
            placeholder="Mô tả về không gian nhà hàng, món ăn đặc sắc, phong cách phục vụ, điểm nổi bật của nhà hàng..."
            maxLength={500}
          />
          <div className="flex justify-between items-center mt-1">
            {errors.description && <p className="text-sm text-red-600">{errors.description}</p>}
            <p className={`text-xs ml-auto ${formData.description.length < 20 ? 'text-red-500' : 'text-gray-500'}`}>
              {formData.description.length}/500 (tối thiểu 20 ký tự)
            </p>
          </div>
        </div>

        {/* Price Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Mức giá trung bình
            <span className="text-xs text-gray-500 ml-2">(Giúp khách hàng có kỳ vọng phù hợp)</span>
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {priceRanges.map(range => (
              <div
                key={range.value}
                onClick={() => handleInputChange('price_range', range.value)}
                className={`
                  p-6 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md text-center
                  ${formData.price_range === range.value 
                    ? `border-${range.color}-500 bg-${range.color}-50 shadow-md` 
                    : 'border-gray-200 hover:border-gray-300'
                  }
                `}
              >
                <div className="text-3xl mb-2">{range.icon}</div>
                <div className="font-bold text-gray-900 text-lg">{range.label}</div>
                <div className="text-sm text-gray-600 mt-1">{range.description}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const Step2 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Địa chỉ và thông tin liên hệ</h2>
        <p className="text-gray-600">Giúp khách hàng tìm thấy và liên hệ với nhà hàng</p>
      </div>

      {/* Address Section */}
      <div className="bg-blue-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-blue-900 mb-4 flex items-center">
          <MapPin className="w-5 h-5 mr-2" />
          Địa chỉ nhà hàng
        </h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Địa chỉ đầy đủ *
            </label>
            <input
              type="text"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              className={`
                w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                ${errors.address ? 'border-red-500 bg-red-50' : 'border-gray-300'}
              `}
              placeholder="VD: 123 Trần Hưng Đạo, Phường Hội Thương, TP Pleiku"
            />
            {errors.address && <p className="mt-1 text-sm text-red-600">{errors.address}</p>}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tỉnh/Thành phố *
              </label>
              <select
                value={formData.province}
                onChange={(e) => handleInputChange('province', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {provinces.map(province => (
                  <option key={province} value={province}>{province}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quận/Huyện
              </label>
              <input
                type="text"
                value={formData.district}
                onChange={(e) => handleInputChange('district', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="VD: TP Pleiku, Chư Prông..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phường/Xã
              </label>
              <input
                type="text"
                value={formData.ward}
                onChange={(e) => handleInputChange('ward', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="VD: Hội Thương, Yên Đỗ..."
              />
            </div>
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div className="bg-green-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-green-900 mb-4 flex items-center">
          <Phone className="w-5 h-5 mr-2" />
          Thông tin liên hệ
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Số điện thoại
              <span className="text-xs text-gray-500 ml-2">(Khách hàng có thể gọi đặt bàn)</span>
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              className={`
                w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                ${errors.phone ? 'border-red-500 bg-red-50' : 'border-gray-300'}
              `}
              placeholder="VD: 0269.123.456 hoặc +84 269 123 456"
            />
            {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
              <span className="text-xs text-gray-500 ml-2">(Để nhận đánh giá và phản hồi)</span>
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              className={`
                w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                ${errors.email ? 'border-red-500 bg-red-50' : 'border-gray-300'}
              `}
              placeholder="VD: contact@nhahang.com"
            />
            {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
          </div>
        </div>

        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Website (không bắt buộc)
          </label>
          <input
            type="url"
            value={formData.website}
            onChange={(e) => handleInputChange('website', e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="VD: https://nhahang.com"
          />
        </div>
      </div>

      {/* Social Media */}
      <div className="bg-purple-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-purple-900 mb-4 flex items-center">
          <Globe className="w-5 h-5 mr-2" />
          Mạng xã hội (không bắt buộc)
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
              <Facebook className="w-4 h-4 mr-2 text-blue-600" />
              Facebook Page
            </label>
            <input
              type="url"
              value={formData.social_media.facebook}
              onChange={(e) => handleInputChange('social_media.facebook', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="VD: https://facebook.com/nhahang"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
              <Instagram className="w-4 h-4 mr-2 text-pink-600" />
              Instagram
            </label>
            <input
              type="url"
              value={formData.social_media.instagram}
              onChange={(e) => handleInputChange('social_media.instagram', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="VD: https://instagram.com/nhahang"
            />
          </div>
        </div>
      </div>

      {/* Map Preview */}
      <div className="bg-gray-100 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
          <Map className="w-5 h-5 mr-2" />
          Vị trí trên bản đồ
        </h3>
        <div className="bg-white h-64 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <MapPin className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 font-medium">Bản đồ tương tác sẽ hiển thị ở đây</p>
            <p className="text-sm text-gray-500 mt-2">
              {formData.address ? `📍 ${formData.address}` : 'Nhập địa chỉ để hiển thị vị trí'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const Step3 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Hình ảnh nhà hàng</h2>
        <p className="text-gray-600">Hình ảnh đẹp sẽ thu hút và tạo ấn tượng tốt với khách hàng</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Logo Upload */}
        <FileUpload
          type="logo"
          label="Logo nhà hàng"
          className="space-y-2"
        />

        {/* Cover Image Upload */}
        <FileUpload
          type="cover"
          label="Ảnh bìa nhà hàng"
          className="space-y-2"
        />
      </div>

      {/* Gallery Images */}
      <div className="bg-orange-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-orange-900 mb-4 flex items-center">
          <Camera className="w-5 h-5 mr-2" />
          Thư viện ảnh món ăn
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          {formData.gallery_images.map((url, index) => (
            <div key={index} className="relative group">
              <img 
                src={url} 
                alt={`Gallery ${index + 1}`} 
                className="w-full h-24 rounded-lg object-cover border-2 border-white shadow-sm group-hover:shadow-md transition-shadow"
              />
              <button
                onClick={() => {
                  const newGallery = formData.gallery_images.filter((_, i) => i !== index);
                  handleInputChange('gallery_images', newGallery);
                }}
                className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
          
          {/* Add new image button */}
          {formData.gallery_images.length < 10 && (
            <FileUpload
              type="gallery"
              label=""
              className="h-24"
            />
          )}
        </div>
        
        <div className="bg-white p-4 rounded-lg border border-orange-200">
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center flex-shrink-0">
              <Camera className="w-4 h-4 text-orange-600" />
            </div>
            <div>
              <h4 className="text-sm font-medium text-orange-900">💡 Mẹo chụp ảnh món ăn hiệu quả:</h4>
              <ul className="text-sm text-orange-700 mt-2 space-y-1">
                <li>• Chụp ảnh dưới ánh sáng tự nhiên (gần cửa sổ)</li>
                <li>• Bố cục đẹp mắt, có thể thêm đồ trang trí</li>
                <li>• Chụp từ góc 45° hoặc từ trên xuống</li>
                <li>• Đảm bảo ảnh rõ nét, không bị mờ</li>
                <li>• Thêm {Math.max(0, 3 - formData.gallery_images.length)} ảnh nữa để đạt tối thiểu 3 ảnh</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const Step4 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">AI tối ưu hóa nội dung</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Trí tuệ nhân tạo sẽ giúp bạn tạo mô tả hấp dẫn, gợi ý menu phù hợp và tối ưu SEO để thu hút khách hàng
        </p>
      </div>

      <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 p-8 rounded-2xl border border-purple-200">
        <div className="flex items-center mb-6">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={formData.enable_ai_enhancement}
              onChange={(e) => handleInputChange('enable_ai_enhancement', e.target.checked)}
              className="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
            />
            <span className="ml-3 text-xl font-bold text-gray-900">
              🚀 Kích hoạt AI Enhancement
            </span>
          </label>
        </div>

        {formData.enable_ai_enhancement ? (
          <div className="space-y-6">
            {errors.ai && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2" />
                {errors.ai}
              </div>
            )}

            {isLoading ? (
              <div className="text-center py-12">
                <div className="relative mx-auto w-24 h-24 mb-6">
                  <div className="absolute inset-0 rounded-full border-4 border-purple-200"></div>
                  <div className="absolute inset-0 rounded-full border-4 border-purple-600 border-t-transparent animate-spin"></div>
                  <div className="absolute inset-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-white animate-pulse" />
                  </div>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">AI đang phân tích và tối ưu...</h3>
                <p className="text-gray-600 mb-4">Vui lòng chờ trong giây lát</p>
                <div className="max-w-md mx-auto bg-white rounded-full p-1 shadow-inner">
                  <div className="bg-gradient-to-r from-purple-500 to-blue-500 rounded-full h-2 transition-all duration-1000" style={{width: '75%'}}></div>
                </div>
              </div>
            ) : aiEnhancement ? (
              <div className="space-y-6">
                <div className="bg-white rounded-xl p-6 shadow-sm border-2 border-green-200">
                  <div className="flex items-center text-green-600 mb-4">
                    <CheckCircle className="w-6 h-6 mr-2" />
                    <span className="font-bold text-lg">✨ AI đã hoàn thành tối ưu hóa!</span>
                    <span className="text-sm text-gray-500 ml-2">({aiEnhancement.processing_time}s)</span>
                  </div>
                  
                  {aiEnhancement.suggestions && (
                    <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h4 className="font-medium text-blue-900 mb-2">💡 Gợi ý cải thiện:</h4>
                      <ul className="space-y-1 text-sm text-blue-800">
                        {aiEnhancement.suggestions.map((suggestion, index) => (
                          <li key={index}>• {suggestion}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Enhanced Description */}
                <div className="bg-white rounded-xl p-6 shadow-sm border">
                  <h4 className="font-bold text-gray-900 mb-3 flex items-center">
                    <span className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">📝</span>
                    Mô tả được cải thiện
                  </h4>
                  <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-green-500">
                    <p className="text-gray-800 leading-relaxed">{aiEnhancement.enhanced_description}</p>
                  </div>
                </div>

                {/* Menu Suggestions */}
                <div className="bg-white rounded-xl p-6 shadow-sm border">
                  <h4 className="font-bold text-gray-900 mb-3 flex items-center">
                    <span className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center mr-3">🍽️</span>
                    Gợi ý menu phù hợp
                  </h4>
                  <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-orange-500">
                    <div className="text-gray-800 text-sm leading-relaxed whitespace-pre-line">
                      {aiEnhancement.menu_suggestions}
                    </div>
                  </div>
                </div>

                {/* SEO Content */}
                <div className="bg-white rounded-xl p-6 shadow-sm border">
                  <h4 className="font-bold text-gray-900 mb-3 flex items-center">
                    <span className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">🔍</span>
                    Tối ưu SEO
                  </h4>
                  <div className="space-y-4 text-sm">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <div className="font-medium text-gray-700 mb-1">📄 Tiêu đề trang:</div>
                        <div className="bg-gray-50 p-3 rounded border text-gray-800">
                          {aiEnhancement.seo_content.title}
                        </div>
                      </div>
                      <div>
                        <div className="font-medium text-gray-700 mb-1">📱 Tiêu đề mạng xã hội:</div>
                        <div className="bg-gray-50 p-3 rounded border text-gray-800">
                          {aiEnhancement.seo_content.social_title}
                        </div>
                      </div>
                    </div>
                    <div>
                      <div className="font-medium text-gray-700 mb-1">📝 Mô tả meta:</div>
                      <div className="bg-gray-50 p-3 rounded border text-gray-800">
                        {aiEnhancement.seo_content.meta_description}
                      </div>
                    </div>
                    <div>
                      <div className="font-medium text-gray-700 mb-1">🏷️ Từ khóa chính:</div>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {aiEnhancement.seo_content.keywords.slice(0, 6).map((keyword, index) => (
                          <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="w-24 h-24 bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <Sparkles className="w-12 h-12 text-purple-500" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Sẵn sàng tối ưu hóa nội dung!</h3>
                <p className="text-gray-600 mb-6 max-w-md mx-auto">
                  AI sẽ phân tích thông tin nhà hàng và tạo nội dung chuyên nghiệp, hấp dẫn khách hàng
                </p>
                <div className="space-y-4">
                  <div className="bg-white rounded-lg p-4 border-2 border-dashed border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                      <div>
                        <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-2xl">📝</span>
                        </div>
                        <div className="font-medium text-green-800">Mô tả hấp dẫn</div>
                        <div className="text-xs text-green-600">Viết lại chuyên nghiệp</div>
                      </div>
                      <div>
                        <div className="w-  //import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, MapPin, Star, Sparkles, CheckCircle, AlertCircle, 
  Clock, Wifi, Car, Utensils, X, Plus, Camera, Map, Phone,
  Mail, Globe, Instagram, Facebook, ChevronRight, ChevronLeft,
  Loader2, Check, AlertTriangle, Info
} from 'lucide-react';

const RestaurantCreationForm = () => {
  // Form state
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    // Thông tin cơ bản
    name: '',
    description: '',
    cuisine_type: '',
    
    // Địa chỉ
    address: '',
    province: 'Gia Lai',
    district: '',
    ward: '',
    longitude: null,
    latitude: null,
    
    // Hình ảnh
    logo_url: '',
    cover_image_url: '',
    gallery_images: [],
    
    // Thông tin kinh doanh
    opening_hours: {
      monday: '',
      tuesday: '',
      wednesday: '',
      thursday: '',
      friday: '',
      saturday: '',
      sunday: ''
    },
    price_range: 'medium',
    facilities: [],
    
    // Liên hệ
    phone: '',
    email: '',
    website: '',
    social_media: {
      facebook: '',
      instagram: ''
    },
    
    // AI settings
    enable_ai_enhancement: true
  });

  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [aiEnhancement, setAiEnhancement] = useState(null);
  const [errors, setErrors] = useState({});
  const [uploadProgress, setUploadProgress] = useState({});
  const [showSuccess, setShowSuccess] = useState(false);
  const [mapLocation, setMapLocation] = useState(null);

  // File input refs
  const logoInputRef = useRef(null);
  const coverInputRef = useRef(null);
  const galleryInputRef = useRef(null);

  // Constants
  const totalSteps = 6;
  
  const cuisineTypes = [
    { value: 'Việt Nam', label: 'Ẩm thực Việt Nam', emoji: '🇻🇳' },
    { value: 'Nhật Bản', label: 'Ẩm thực Nhật Bản', emoji: '🇯🇵' },
    { value: 'Hàn Quốc', label: 'Ẩm thực Hàn Quốc', emoji: '🇰🇷' },
    { value: 'Trung Hoa', label: 'Ẩm thực Trung Hoa', emoji: '🇨🇳' },
    { value: 'Thái Lan', label: 'Ẩm thực Thái Lan', emoji: '🇹🇭' },
    { value: 'Âu', label: 'Ẩm thực châu Âu', emoji: '🇪🇺' },
    { value: 'Mỹ', label: 'Ẩm thực Mỹ', emoji: '🇺🇸' },
    { value: 'Ấn Độ', label: 'Ẩm thực Ấn Độ', emoji: '🇮🇳' },
    { value: 'Lẩu', label: 'Lẩu & Nướng', emoji: '🍲' },
    { value: 'Fast Food', label: 'Fast Food', emoji: '🍔' },
    { value: 'Cafe', label: 'Cafe & Đồ uống', emoji: '☕' },
    { value: 'Bánh ngọt', label: 'Bánh ngọt & Dessert', emoji: '🧁' },
    { value: 'Chay', label: 'Ẩm thực chay', emoji: '🥬' },
    { value: 'Hải sản', label: 'Hải sản tươi sống', emoji: '🦐' }
  ];

  const facilityOptions = [
    { key: 'wifi', label: 'WiFi miễn phí', icon: Wifi, color: 'blue' },
    { key: 'parking', label: 'Chỗ đỗ xe', icon: Car, color: 'green' },
    { key: 'outdoor_seating', label: 'Chỗ ngồi ngoài trời', icon: Utensils, color: 'orange' },
    { key: 'air_conditioning', label: 'Điều hòa không khí', icon: Clock, color: 'cyan' },
    { key: 'takeaway', label: 'Phục vụ mang về', icon: CheckCircle, color: 'purple' },
    { key: 'delivery', label: 'Giao hàng tận nơi', icon: CheckCircle, color: 'pink' },
    { key: 'credit_card', label: 'Thanh toán thẻ', icon: CheckCircle, color: 'indigo' },
    { key: 'live_music', label: 'Nhạc sống', icon: CheckCircle, color: 'red' }
  ];

  const priceRanges = [
    { 
      value: 'cheap', 
      label: 'Bình dân', 
      description: 'Dưới 100k/người',
      icon: '💰',
      color: 'green'
    },
    { 
      value: 'medium', 
      label: 'Trung bình', 
      description: '100k-300k/người',
      icon: '💎',
      color: 'blue'
    },
    { 
      value: 'expensive', 
      label: 'Cao cấp', 
      description: 'Trên 300k/người',
      icon: '👑',
      color: 'purple'
    }
  ];

  const provinces = [
    'Gia Lai', 'TP.HCM', 'Hà Nội', 'Đà Nẵng', 'Cần Thơ', 
    'Hải Phòng', 'Biên Hòa', 'Nha Trang', 'Huế', 'Đà Lạt'
  ];

  const steps = [
    { 
      id: 1, 
      title: 'Thông tin cơ bản', 
      description: 'Tên nhà hàng và loại ẩm thực',
      icon: Info
    },
    { 
      id: 2, 
      title: 'Địa chỉ & liên hệ', 
      description: 'Vị trí và thông tin liên lạc',
      icon: MapPin
    },
    { 
      id: 3, 
      title: 'Hình ảnh', 
      description: 'Logo, ảnh bìa và thư viện',
      icon: Camera
    },
    { 
      id: 4, 
      title: 'AI tối ưu hóa', 
      description: 'Để AI cải thiện nội dung',
      icon: Sparkles
    },
    { 
      id: 5, 
      title: 'Chi tiết kinh doanh', 
      description: 'Giờ mở cửa và tiện ích',
      icon: Clock
    },
    { 
      id: 6, 
      title: 'Xem trước & hoàn tất', 
      description: 'Kiểm tra và tạo nhà hàng',
      icon: CheckCircle
    }
  ];

  // Utility functions
  const handleInputChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      setFormData(prev => ({ ...prev, [field]: value }));
    }
    
    // Clear error for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const handleFacilityToggle = (facility) => {
    setFormData(prev => ({
      ...prev,
      facilities: prev.facilities.includes(facility)
        ? prev.facilities.filter(f => f !== facility)
        : [...prev.facilities, facility]
    }));
  };

  const validateStep = (step) => {
    const newErrors = {};
    
    switch (step) {
      case 1:
        if (!formData.name?.trim()) newErrors.name = 'Vui lòng nhập tên nhà hàng';
        if (formData.name?.length < 2) newErrors.name = 'Tên nhà hàng phải có ít nhất 2 ký tự';
        if (!formData.cuisine_type) newErrors.cuisine_type = 'Vui lòng chọn loại ẩm thực';
        if (!formData.description?.trim()) newErrors.description = 'Vui lòng nhập mô tả nhà hàng';
        if (formData.description?.length < 20) newErrors.description = 'Mô tả phải có ít nhất 20 ký tự';
        break;
        
      case 2:
        if (!formData.address?.trim()) newErrors.address = 'Vui lòng nhập địa chỉ';
        if (!formData.province) newErrors.province = 'Vui lòng chọn tỉnh/thành phố';
        if (formData.phone && !/^[0-9+\-\s()]{8,15}$/.test(formData.phone)) {
          newErrors.phone = 'Số điện thoại không hợp lệ';
        }
        if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          newErrors.email = 'Email không hợp lệ';
        }
        break;
        
      case 5:
        const hasOpeningHours = Object.values(formData.opening_hours).some(hour => hour?.trim());
        if (!hasOpeningHours) {
          newErrors.opening_hours = 'Vui lòng nhập giờ mở cửa cho ít nhất một ngày';
        }
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // File upload handling
  const handleFileUpload = async (type, files) => {
    if (!files || files.length === 0) return;
    
    setUploadProgress(prev => ({ ...prev, [type]: 0 }));
    
    try {
      const file = files[0];
      
      // Validate file
      if (!file.type.startsWith('image/')) {
        throw new Error('Vui lòng chọn file hình ảnh');
      }
      
      if (file.size > 5 * 1024 * 1024) { // 5MB
        throw new Error('File không được vượt quá 5MB');
      }

      // Mock upload process with progress
      const uploadPromise = new Promise((resolve, reject) => {
        let progress = 0;
        const interval = setInterval(() => {
          progress += Math.random() * 30;
          setUploadProgress(prev => ({ ...prev, [type]: Math.min(progress, 90) }));
          
          if (progress >= 90) {
            clearInterval(interval);
            // Simulate final upload completion
            setTimeout(() => {
              setUploadProgress(prev => ({ ...prev, [type]: 100 }));
              resolve({
                url: URL.createObjectURL(file), // Tạo temporary URL cho preview
                filename: file.name,
                size: file.size
              });
            }, 500);
          }
        }, 100);
      });

      const result = await uploadPromise;
      
      if (type === 'gallery') {
        setFormData(prev => ({
          ...prev,
          gallery_images: [...prev.gallery_images, result.url]
        }));
      } else {
        setFormData(prev => ({ ...prev, [`${type}_url`]: result.url }));
      }
      
      // Clear progress after delay
      setTimeout(() => {
        setUploadProgress(prev => ({ ...prev, [type]: null }));
      }, 1000);
      
    } catch (error) {
      console.error('Upload failed:', error);
      setErrors(prev => ({ ...prev, [type]: error.message }));
      setUploadProgress(prev => ({ ...prev, [type]: null }));
    }
  };

  // AI Enhancement
  const requestAIEnhancement = async () => {
    setIsLoading(true);
    
    try {
      // Mock AI enhancement call
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const mockEnhancement = {
        enhanced_description: `${formData.name} là điểm đến ẩm thực ${formData.cuisine_type.toLowerCase()} đặc biệt tại ${formData.address}. Với không gian ${formData.price_range === 'expensive' ? 'sang trọng và đẳng cấp' : formData.price_range === 'cheap' ? 'ấm cúng và thân thiện' : 'hiện đại và thoải mái'}, nhà hàng mang đến trải nghiệm ẩm thực khó quên. Đội ngũ đầu bếp giàu kinh nghiệm kết hợp nguyên liệu tươi ngon và công thức độc đáo để tạo nên những món ăn tinh tế. ${formData.facilities.includes('outdoor_seating') ? 'Khu vực outdoor lãng mạn phù hợp cho các buổi hẹn hò.' : ''} ${formData.facilities.includes('parking') ? 'Bãi đỗ xe rộng rãi, thuận tiện cho thực khách.' : ''} Hãy đến và cảm nhận sự khác biệt tại ${formData.name}!`,
        
        menu_suggestions: `**🍽️ MENU ĐỀ XUẤT CHO ${formData.name.toUpperCase()}**

**KHAI VỊ**
${formData.cuisine_type === 'Việt Nam' 
  ? `- Gỏi cuốn tươi (${formData.price_range === 'expensive' ? '65k' : formData.price_range === 'medium' ? '45k' : '35k'}): Bánh tráng mỏng cuốn tôm thịt, rau thơm
- Chả cá nướng lá chuối (${formData.price_range === 'expensive' ? '85k' : formData.price_range === 'medium' ? '65k' : '45k'}): Cá tra tươi nướng thơm lừng` 
  : formData.cuisine_type === 'Nhật Bản'
  ? `- Sashimi cá hồi (${formData.price_range === 'expensive' ? '150k' : formData.price_range === 'medium' ? '120k' : '95k'}): Cá hồi Na Uy tươi ngon
- Gyoza chiên (${formData.price_range === 'expensive' ? '85k' : formData.price_range === 'medium' ? '65k' : '45k'}): Bánh xếp Nhật pan chiên giòn`
  : `- Món khai vị đặc trưng (${formData.price_range === 'expensive' ? '80k' : formData.price_range === 'medium' ? '60k' : '40k'})
- Soup đặc sản (${formData.price_range === 'expensive' ? '70k' : formData.price_range === 'medium' ? '50k' : '35k'})`
}

**MÓN CHÍNH**
${formData.cuisine_type === 'Việt Nam'
  ? `- Phở bò đặc biệt (${formData.price_range === 'expensive' ? '120k' : formData.price_range === 'medium' ? '85k' : '65k'}): Nước dùng ninh 12 tiếng
- Bún bò Huế cay (${formData.price_range === 'expensive' ? '110k' : formData.price_range === 'medium' ? '75k' : '55k'}): Đậm đà hương vị cố đô`
  : formData.cuisine_type === 'Nhật Bản'
  ? `- Sushi set premium (${formData.price_range === 'expensive' ? '350k' : formData.price_range === 'medium' ? '250k' : '180k'}): 12 miếng sushi cao cấp
- Ramen tonkotsu (${formData.price_range === 'expensive' ? '180k' : formData.price_range === 'medium' ? '130k' : '95k'}): Nước dùng xương heo đậm đà`
  : `- Món chính signature (${formData.price_range === 'expensive' ? '250k' : formData.price_range === 'medium' ? '150k' : '95k'})
- Combo set đặc biệt (${formData.price_range === 'expensive' ? '320k' : formData.price_range === 'medium' ? '220k' : '150k'})`
}

🌟 **MÓN SIGNATURE KHÔNG THỂ BỎ LỞ:**
- Đặc sản ${formData.name} - Công thức độc quyền được nhiều thực khách yêu thích
- ${formData.cuisine_type} fusion - Sự kết hợp độc đáo giữa truyền thống và hiện đại`,

        seo_content: {
          title: `${formData.name} - Nhà hàng ${formData.cuisine_type} ${formData.district ? formData.district + ', ' : ''}${formData.province}`,
          meta_description: `Thưởng thức ẩm thực ${formData.cuisine_type} đặc sắc tại ${formData.name}. ${formData.address}. Không gian ${formData.price_range === 'expensive' ? 'sang trọng' : 'ấm cúng'}, món ăn ngon, phục vụ tận tâm. Đặt bàn ngay!`,
          keywords: [
            formData.name.toLowerCase(),
            `nhà hàng ${formData.cuisine_type.toLowerCase()}`,
            `${formData.cuisine_type.toLowerCase()} ${formData.province.toLowerCase()}`,
            `ăn ${formData.cuisine_type.toLowerCase()} ${formData.district?.toLowerCase() || formData.province.toLowerCase()}`,
            'nhà hàng ngon',
            `${formData.price_range === 'expensive' ? 'nhà hàng cao cấp' : formData.price_range === 'cheap' ? 'nhà hàng bình dân' : 'nhà hàng gia đình'}`,
            formData.district?.toLowerCase(),
            formData.province.toLowerCase()
          ],
          social_title: `🍽️ ${formData.name} - ${formData.cuisine_type} Đặc Sắc`,
          social_description: `Khám phá hương vị ${formData.cuisine_type} tuyệt vời tại ${formData.name}! 📍 ${formData.address} ⭐ Đánh giá cao từ thực khách`
        },
        processing_time: 2.8,
        suggestions: [
          `💡 Nên thêm ảnh ${formData.cuisine_type === 'Nhật Bản' ? 'sushi và sashimi' : formData.cuisine_type === 'Việt Nam' ? 'phở và các món truyền thống' : 'các món đặc trưng'} vào thư viện`,
          `📱 Tạo trang Facebook để tương tác với khách hàng`,
          `🎯 Focus vào từ khóa "${formData.cuisine_type.toLowerCase()} ${formData.province.toLowerCase()}" để SEO tốt hơn`,
          formData.facilities.length < 3 ? '🏪 Bổ sung thêm tiện ích để thu hút khách hàng' : null
        ].filter(Boolean)
      };
      
      setAiEnhancement(mockEnhancement);
      
    } catch (error) {
      console.error('AI Enhancement failed:', error);
      setErrors(prev => ({ ...prev, ai: 'Có lỗi xảy ra khi xử lý AI. Vui lòng thử lại.' }));
    } finally {
      setIsLoading(false);
    }
  };

  // Navigation
  const handleNext = async () => {
    if (!validateStep(currentStep)) return;
    
    // Special handling for AI step
    if (currentStep === 4 && formData.enable_ai_enhancement && !aiEnhancement && !isLoading) {
      await requestAIEnhancement();
      return;
    }
    
    setCurrentStep(prev => Math.min(prev + 1, totalSteps));
  };

  const handlePrevious = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  // Submit
  const handleSubmit = async () => {
    if (!validateStep(6)) return;

    setIsLoading(true);
    
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      console.log('Creating restaurant:', {
        ...formData,
        ai_enhancement: aiEnhancement
      });
      
      setShowSuccess(true);
      
      // Redirect after showing success
      setTimeout(() => {
        // window.location.href = '/dashboard';
        console.log('Redirecting to dashboard...');
      }, 2000);
      
    } catch (error) {
      console.error('Create restaurant failed:', error);
      setErrors(prev => ({ ...prev, submit: 'Có lỗi xảy ra khi tạo nhà hàng. Vui lòng thử lại.' }));
    } finally {
      setIsLoading(false);
    }
  };

  // Success Modal
  const SuccessModal = () => (
    showSuccess && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl p-8 max-w-md w-full text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">🎉 Tạo nhà hàng thành công!</h2>
          <p className="text-gray-600 mb-6">
            Nhà hàng "{formData.name}" đã được tạo thành công. 
            Bạn sẽ được chuyển đến dashboard để quản lý.
          </p>
          <div className="animate-pulse text-blue-600">
            Đang chuyển hướng...
          </div>
        </div>
      </div>
    )
  );

  // Render step indicator
  const StepIndicator = () => (
    <div className="mb-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const IconComponent = step.icon;
          const isActive = currentStep === step.id;
          const isCompleted = currentStep > step.id;
          const isAccessible = currentStep >= step.id;
          
          return (
            <div key={step.id} className="flex items-center">
              <div 
                className={`
                  relative flex items-center justify-center w-10 h-10 rounded-full border-2 text-sm font-medium transition-all cursor-pointer
                  ${isActive 
                    ? 'bg-blue-600 border-blue-600 text-white shadow-lg scale-110' 
                    : isCompleted
                    ? 'bg-green-600 border-green-600 text-white'
                    : isAccessible
                    ? 'bg-white border-blue-300 text-blue-600 hover:border-blue-500'
                    : 'bg-gray-100 border-gray-300 text-gray-400'
                  }
                `}
                onClick={() => isAccessible && setCurrentStep(step.id)}
              >
                {isCompleted ? (
                  <Check className="w-5 h-5" />
                ) : (
                  <IconComponent className="w-5 h-5" />
                )}
                {isActive && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
                )}
              </div>
              
              {index < steps.length - 1 && (
                <div className={`
                  w-12 h-1 mx-2 rounded-full transition-all
                  ${currentStep > step.id ? 'bg-green-600' : 'bg-gray-200'}
                `} />
              )}
            </div>
          );
        })}
      </div>
      
      <div className="mt-4 text-center">
        <h3 className="text-lg font-medium text-gray-900">{steps[currentStep - 1]?.title}</h3>
        <p className="text-sm text-gray-600">{steps[currentStep - 1]?.description}</p>
      </div>
    </div>
  );

                        <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-2xl">🍽️</span>
                        </div>
                        <div className="font-medium text-orange-800">Gợi ý menu</div>
                        <div className="text-xs text-orange-600">Phù hợp loại ẩm thực</div>
                      </div>
                      <div>
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-2xl">🔍</span>
                        </div>
                        <div className="font-medium text-blue-800">Tối ưu SEO</div>
                        <div className="text-xs text-blue-600">Dễ tìm thấy hơn</div>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={requestAIEnhancement}
                    className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                  >
                    <Sparkles className="w-5 h-5 inline mr-2" />
                    Bắt đầu AI Enhancement
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertCircle className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">AI Enhancement đã tắt</h3>
            <p className="text-gray-600 mb-4">
              Bạn có thể bật lại bất cứ lúc nào để AI giúp tối ưu nội dung nhà hàng
            </p>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-md mx-auto">
              <div className="flex items-start">
                <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-yellow-800">
                  <div className="font-medium">Lưu ý:</div>
                  <div className="mt-1">AI có thể giúp tạo mô tả hấp dẫn hơn 3-5 lần và gợi ý menu phù hợp, giúp thu hút khách hàng hiệu quả hơn.</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const Step5 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Chi tiết kinh doanh</h2>
        <p className="text-gray-600">Thông tin về giờ mở cửa và các tiện ích phục vụ</p>
      </div>

      {/* Opening Hours */}
      <div className="bg-blue-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-blue-900 mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2" />
          Giờ mở cửa *
        </h3>
        
        <div className="space-y-3">
          {[
            { key: 'monday', label: 'Thứ Hai', emoji: '📅' },
            { key: 'tuesday', label: 'Thứ Ba', emoji: '📅' },
            { key: 'wednesday', label: 'Thứ Tư', emoji: '📅' },
            { key: 'thursday', label: 'Thứ Năm', emoji: '📅' },
            { key: 'friday', label: 'Thứ Sáu', emoji: '📅' },
            { key: 'saturday', label: 'Thứ Bảy', emoji: '🎉' },
            { key: 'sunday', label: 'Chủ Nhật', emoji: '🌞' }
          ].map(day => (
            <div key={day.key} className="flex items-center space-x-4 bg-white p-3 rounded-lg border">
              <div className="flex items-center w-24">
                <span className="mr-2">{day.emoji}</span>
                <span className="text-sm font-medium text-gray-700">{day.label}:</span>
              </div>
              <input
                type="text"
                value={formData.opening_hours[day.key] || ''}
                onChange={(e) => handleInputChange(`opening_hours.${day.key}`, e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
                placeholder="VD: 08:00-22:00, 08:00-14:00,17:00-22:00, hoặc 'Đóng cửa'"
              />
            </div>
          ))}
        </div>
        
        {errors.opening_hours && <p className="mt-3 text-sm text-red-600">{errors.opening_hours}</p>}
        
        <div className="mt-4 bg-white p-4 rounded-lg border border-blue-200">
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
              <Info className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <h4 className="text-sm font-medium text-blue-900">💡 Hướng dẫn nhập giờ mở cửa:</h4>
              <ul className="text-sm text-blue-700 mt-2 space-y-1">
                <li>• <strong>Cả ngày:</strong> 08:00-22:00</li>
                <li>• <strong>Nghỉ trưa:</strong> 08:00-14:00,17:00-22:00</li>
                <li>• <strong>Ngày nghỉ:</strong> Đóng cửa</li>
                <li>• <strong>24/7:</strong> 00:00-23:59</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Facilities */}
      <div className="bg-green-50 p-6 rounded-lg">
        <h3 className="text-lg font-medium text-green-900 mb-4 flex items-center">
          <CheckCircle className="w-5 h-5 mr-2" />
          Tiện ích & dịch vụ
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {facilityOptions.map(facility => {
            const IconComponent = facility.icon;
            const isSelected = formData.facilities.includes(facility.key);
            
            return (
              <div
                key={facility.key}
                onClick={() => handleFacilityToggle(facility.key)}
                className={`
                  p-4 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md
                  ${isSelected
                    ? `border-${facility.color}-500 bg-${facility.color}-50 shadow-md`
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                  }
                `}
              >
                <div className="text-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-2 ${
                    isSelected ? `bg-${facility.color}-100` : 'bg-gray-100'
                  }`}>
                    <IconComponent className={`w-5 h-5 ${
                      isSelected ? `text-${facility.color}-600` : 'text-gray-500'
                    }`} />
                  </div>
                  <div className={`text-sm font-medium ${
                    isSelected ? `text-${facility.color}-900` : 'text-gray-700'
                  }`}>
                    {facility.label}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        <div className="mt-4 text-center">
          <p className="text-sm text-green-700">
            ✅ Đã chọn {formData.facilities.length} tiện ích
            {formData.facilities.length === 0 && " (Hãy chọn các tiện ích có tại nhà hàng)"}
          </p>
        </div>
      </div>
    </div>
  );

  const Step6 = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Xem trước & hoàn tất</h2>
        <p className="text-gray-600">Kiểm tra lại thông tin trước khi tạo nhà hàng</p>
      </div>

      {/* Restaurant Preview Card */}
      <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-lg">
        {/* Cover Image */}
        {formData.cover_image_url && (
          <div className="relative h-48 bg-gradient-to-r from-blue-500 to-purple-600">
            <img 
              src={formData.cover_image_url} 
              alt="Cover" 
              className="w-full h-full object-cover"
            />
            <div className="absolute top-4 right-4 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
              🖼️ Ảnh bìa
            </div>
          </div>
        )}
        
        <div className="p-6">
          {/* Header */}
          <div className="flex items-start space-x-4 mb-6">
            {formData.logo_url ? (
              <img 
                src={formData.logo_url} 
                alt="Logo" 
                className="w-16 h-16 rounded-xl object-cover border-3 border-white shadow-md"
              />
            ) : (
              <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🏪</span>
              </div>
            )}
            
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h3 className="text-2xl font-bold text-gray-900">{formData.name}</h3>
                <span className="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full font-medium">
                  {cuisineTypes.find(c => c.value === formData.cuisine_type)?.emoji} {formData.cuisine_type}
                </span>
              </div>
              
              <div className="flex items-center space-x-4 text-gray-600 text-sm">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {formData.address}
                </div>
                <div className="flex items-center">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    formData.price_range === 'cheap' ? 'bg-green-100 text-green-700' :
                    formData.price_range === 'expensive' ? 'bg-purple-100 text-purple-700' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {priceRanges.find(p => p.value === formData.price_range)?.icon} {priceRanges.find(p => p.value === formData.price_range)?.label}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Info */}
          {(formData.phone || formData.email) && (
            <div className="flex items-center space-x-6 mb-6 text-sm text-gray-600">
              {formData.phone && (
                <div className="flex items-center">
                  <Phone className="w-4 h-4 mr-2 text-green-600" />
                  {formData.phone}
                </div>
              )}
              {formData.email && (
                <div className="flex items-center">
                  <Mail className="w-4 h-4 mr-2 text-blue-600" />
                  {formData.email}
                </div>
              )}
            </div>
          )}

          {/* Description */}
          <div className="mb-6">
            <h4 className="font-medium text-gray-900 mb-3">📝 Mô tả nhà hàng:</h4>
            <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
              <p className="text-gray-700 leading-relaxed">
                {aiEnhancement && formData.enable_ai_enhancement 
                  ? aiEnhancement.enhanced_description 
                  : formData.description
                }
              </p>
            </div>
          </div>

          {/* Gallery Preview */}
          {formData.gallery_images.length > 0 && (
            <div className="mb-6">
              <h4 className="font-medium text-gray-900 mb-3">📸 Thư viện ảnh ({formData.gallery_images.length}):</h4>
              <div className="grid grid-cols-4 md:grid-cols-6 gap-2">
                {formData.gallery_images.slice(0, 6).map((url, index) => (
                  <img 
                    key={index} 
                    src={url} 
                    alt={`Gallery ${index + 1}`} 
                    className="w-full h-16 rounded-lg object-cover border border-gray-200"
                  />
                ))}
                {formData.gallery_images.length > 6 && (
                  <div className="w-full h-16 bg-gray-100 rounded-lg flex items-center justify-center text-gray-600 text-xs font-medium">
                    +{formData.gallery_images.length - 6}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Opening Hours Summary */}
          <div className="mb-6">
            <h4 className="font-medium text-gray-900 mb-3">🕐 Giờ mở cửa:</h4>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                {Object.entries(formData.opening_hours).map(([day, hours]) => 
                  hours && (
                    <div key={day} className="flex justify-between">
                      <span className="text-gray-600 capitalize">
                        {day === 'monday' && 'T2:'}
                        {day === 'tuesday' && 'T3:'}
                        {day === 'wednesday' && 'T4:'}
                        {day === 'thursday' && 'T5:'}
                        {day === 'friday' && 'T6:'}
                        {day === 'saturday' && 'T7:'}
                        {day === 'sunday' && 'CN:'}
                      </span>
                      <span className={`font-medium ${hours === 'Đóng cửa' ? 'text-red-600' : 'text-gray-900'}`}>
                        {hours}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>

          {/* Facilities */}
          {formData.facilities.length > 0 && (
            <div className="mb-6">
              <h4 className="font-medium text-gray-900 mb-3">✨ Tiện ích ({formData.facilities.length}):</h4>
              <div className="flex flex-wrap gap-2">
                {formData.facilities.map(facility => {
                  const facilityInfo = facilityOptions.find(f => f.key === facility);
                  return (
                    <span key={facility} className={`
                      px-3 py-1 rounded-full text-sm font-medium border
                      ${facilityInfo ? `bg-${facilityInfo.color}-100 text-${facilityInfo.color}-700 border-${facilityInfo.color}-200` : 'bg-gray-100 text-gray-700 border-gray-200'}
                    `}>
                      {facilityInfo?.label || facility}
                    </span>
                  );
                })}
              </div>
            </div>
          )}

          {/* AI Enhancement Badge */}
          {aiEnhancement && formData.enable_ai_enhancement && (
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border-2 border-purple-200">
              <div className="flex items-center mb-2">
                <Sparkles className="w-5 h-5 text-purple-600 mr-2" />
                <h4 className="font-bold text-purple-900">🤖 Được tối ưu bởi AI</h4>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                <div className="flex items-center text-green-700">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  Mô tả chuyên nghiệp
                </div>
                <div className="flex items-center text-orange-700">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  Menu gợi ý phù hợp
                </div>
                <div className="flex items-center text-blue-700">
                  <CheckCircle className="w-4 h-4 mr-1" />
                  SEO được tối ưu
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Final confirmation */}
      <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
        <div className="flex items-start space-x-4">
          <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
            <CheckCircle className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <h4 className="font-bold text-green-900 text-lg">🎉 Sẵn sàng tạo nhà hàng!</h4>
            <p className="text-green-700 mt-2">
              Sau khi tạo thành công, bạn sẽ được chuyển đến dashboard để quản lý nhà hàng, xem đánh giá khách hàng, 
              và theo dõi thống kê. Bạn có thể chỉnh sửa thông tin bất cứ lúc nào.
            </p>
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              <div className="flex items-center text-green-800">
                <CheckCircle className="w-4 h-4 mr-2" />
                Dashboard quản lý
              </div>
              <div className="flex items-center text-green-800">
                <CheckCircle className="w-4 h-4 mr-2" />
                Theo dõi đánh giá
              </div>
              <div className="flex items-center text-green-800">
                <CheckCircle className="w-4 h-4 mr-2" />
                Thống kê chi tiết
              </div>
              <div className="flex items-center text-green-800">
                <CheckCircle className="w-4 h-4 mr-2" />
                Chỉnh sửa dễ dàng
              </div>
            </div>
          </div>
        </div>
      </div>

      {errors.submit && (
        <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center">
          <AlertTriangle className="w-5 h-5 mr-2" />
          {errors.submit}
        </div>
      )}
    </div>
  );

  // Main render
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Tạo nhà hàng mới</h1>
            <p className="text-gray-600">Tạo trang nhà hàng chuyên nghiệp với sự hỗ trợ của AI</p>
            <div className="mt-4 text-sm text-gray-500">
              Bước {currentStep} / {totalSteps}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Step Indicator */}
        <StepIndicator />

        {/* Main Form */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          <div className="p-8">
            {/* Step Content */}
            <div className="min-h-[600px]">
              {currentStep === 1 && <Step1 />}
              {currentStep === 2 && <Step2 />}
              {currentStep === 3 && <Step3 />}
              {currentStep === 4 && <Step4 />}
              {currentStep === 5 && <Step5 />}
              {currentStep === 6 && <Step6 />}
            </div>
          </div>

          {/* Navigation Footer */}
          <div className="bg-gray-50 px-8 py-6 border-t border-gray-200">
            <div className="flex justify-between items-center">
              <button
                onClick={handlePrevious}
                disabled={currentStep === 1}
                className={`
                  flex items-center px-6 py-3 rounded-lg font-medium transition-all
                  ${currentStep === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300 hover:shadow-md'
                  }
                `}
              >
                <ChevronLeft className="w-4 h-4 mr-2" />
                Quay lại
              </button>

              <div className="flex items-center space-x-3">
                {/* Save Draft Button (except last step) */}
                {currentStep < totalSteps && (
                  <button className="px-4 py-2 text-gray-600 hover:text-gray-800 text-sm font-medium transition-colors">
                    💾 Lưu nháp
                  </button>
                )}

                {/* Next/Submit Button */}
                {currentStep < totalSteps ? (
                  <button
                    onClick={handleNext}
                    disabled={isLoading}
                    className={`
                      flex items-center px-8 py-3 rounded-lg font-medium transition-all shadow-md
                      ${isLoading
                        ? 'bg-gray-400 text-white cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg transform hover:scale-105'
                      }
                    `}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Đang xử lý...
                      </>
                    ) : (
                      <>
                        Tiếp theo
                        <ChevronRight className="w-4 h-4 ml-2" />
                      </>
                    )}
                  </button>
                ) : (
                  <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className={`
                      flex items-center px-8 py-3 rounded-lg font-bold text-lg transition-all shadow-lg
                      ${isLoading
                        ? 'bg-gray-400 text-white cursor-not-allowed'
                        : 'bg-gradient-to-r from-green-600 to-blue-600 text-white hover:from-green-700 hover:to-blue-700 hover:shadow-xl transform hover:scale-105'
                      }
                    `}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                        Đang tạo nhà hàng...
                      </>
                    ) : (
                      <>
                        🎉 Tạo nhà hàng
                        <Sparkles className="w-5 h-5 ml-2" />
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Help Section */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500 mb-4">
            Cần hỗ trợ? Liên hệ team support của chúng tôi
          </p>
          <div className="flex justify-center space-x-4 text-sm">
            <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
              📞 Hotline: 1900-xxxx
            </a>
            <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
              💬 Live Chat
            </a>
            <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
              📧 Email hỗ trợ
            </a>
          </div>
        </div>
      </div>

      {/* Success Modal */}
      <SuccessModal />
    </div>
  );
};

export default RestaurantCreationForm;
  const FileUpload = ({ type, label, accept = "image/*", multiple = false, className = "" }) => {
    const inputRef = type === 'logo' ? logoInputRef : type === 'cover' ? coverInputRef : galleryInputRef;
    const currentFile = type === 'gallery' ? null : formData[`${type}_url`];
    const progress = uploadProgress[type];
    const error = errors[type];

    return (
      <div className={className}>
        <label className="block text-sm font-medium text-gray-700 mb-2">{label}</label>
        
        <div 
          className={`
            border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all
            ${error ? 'border-red-300 bg-red-50' : currentFile ? 'border-green-300 bg-green-50' : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'}
          `}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept={accept}
            multiple={multiple}
            className="hidden"
            onChange={(e) => handleFileUpload(type, e.target.files)}
          />
          
          {currentFile && type !== 'gallery' ? (
            <div className="relative">
              <img 
                src={currentFile} 
                alt={label}
                className={`mx-auto rounded-lg object-cover ${
                  type === 'logo' ? 'w-24 h-24' : 'w-full h-32'
                }`}
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setFormData(prev => ({ ...prev, [`${type}_url`]: '' }));
                }}
                className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
              >
                <X className="w-3 h-3" />
              </button>
              <div className="mt-2">
                <p className="text-sm font-medium text-green-700">✓ Đã tải lên</p>
              </div>
            </div>
          ) : (
            <>
              <Upload className={`mx-auto mb-2 ${error ? 'text-red-400' : 'text-gray-400'} ${
                type === 'gallery' ? 'w-8 h-8' : 'w-12 h-12'
              }`} />
              <p className={`font-medium ${error ? 'text-red-700' : 'text-gray-700'}`}>
                {type === 'gallery' ? 'Thêm ảnh' : `Tải lên ${label.toLowerCase()}`}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                PNG, JPG, WebP (tối đa 5MB)
              </p>
            </>
          )}
          
          {progress !== null && (
            <div className="mt-3">
              <div className="bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-xs text-gray-600 mt-1">{Math.round(progress)}%</p>
            </div>
          )}
        </div>
        
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>
    );
  };