# 00 - Product Flow Plan

## Product Name
MiMo Voice Studio / VoiceForge AI

## Core Positioning
Không chỉ là Text-to-Speech converter. Đây là AI Voice Studio giúp creator, seller, giáo viên, podcaster và marketer tạo voice-over hoàn chỉnh từ ý tưởng hoặc script.

## Main User Personas

### 1. Content Creator
- Tạo voice-over TikTok/Reels/Shorts.
- Cần giọng tự nhiên, nhanh, nhiều style.
- Cần export file để dùng trong CapCut/Premiere.

### 2. Seller / Marketer
- Tạo voice quảng cáo sản phẩm.
- Cần script ngắn, hook mạnh, CTA rõ.
- Cần nhiều phiên bản A/B.

### 3. Teacher / E-learning Creator
- Biến bài học thành audio.
- Cần giọng rõ ràng, chậm, dễ nghe.
- Cần quản lý nhiều lesson.

### 4. Podcast / Story Creator
- Cần chia đoạn, nhiều speaker, giọng kể chuyện.
- Cần export audio dài.

---

# Core Flows

## Flow A - Quick TTS
1. User đăng nhập.
2. Vào dashboard.
3. Click "New Voice Project".
4. Chọn template "Quick TTS".
5. Nhập text.
6. Chọn voice.
7. Nhập style prompt: ví dụ "giọng nữ trẻ, vui vẻ, tự nhiên".
8. Generate preview.
9. Generate full audio.
10. Lưu audio vào project.
11. Download WAV/MP3.

## Flow B - Script Writer to Voice
1. User nhập ý tưởng thô.
2. Chọn mục tiêu nội dung:
   - TikTok Ads
   - Product Review
   - Podcast Intro
   - Story Narration
   - E-learning
3. AI viết lại script.
4. App tự chia segment.
5. User chỉnh từng segment.
6. Chọn voice/style cho từng segment.
7. Generate từng segment.
8. Ghép audio.
9. Export.

## Flow C - Multi-speaker Dialogue
1. User tạo project dạng "Dialogue".
2. Nhập chủ đề.
3. Chọn số speaker.
4. AI tạo đoạn hội thoại.
5. Mỗi speaker được map với một voice.
6. Generate audio từng câu.
7. Ghép theo thứ tự.
8. Export podcast/dialogue.

## Flow D - Voice Design
1. User vào My Voices.
2. Click "Create Designed Voice".
3. Nhập mô tả giọng:
   - age
   - gender
   - tone
   - accent
   - emotion
   - speaking speed
4. App lưu voice profile.
5. User dùng voice profile trong project.

## Flow E - Voice Clone
1. User vào My Voices.
2. Upload file .wav/.mp3.
3. Tick xác nhận có quyền sử dụng giọng nói.
4. Backend validate file size/duration.
5. Lưu file sample vào storage.
6. Generate bằng MiMo voiceclone khi user dùng.
7. Lưu voice profile.
8. User dùng voice clone trong project.

---

# MVP Scope

## Must Have
- Auth.
- Dashboard.
- Project CRUD.
- Text editor.
- Built-in voice selection.
- Style prompt.
- Preview generation.
- Full generation.
- Audio storage.
- Download audio.
- Usage tracking.
- Basic credit system.

## Should Have
- Segment editor.
- Regenerate segment.
- Project history.
- Format selection WAV/MP3.
- Error handling.
- Job queue.

## Could Have
- Script rewrite.
- Voice design.
- Voice clone.
- Merge audio.
- Stripe payment.

## Not MVP
- Full mobile app.
- Team workspace.
- Realtime collaborative editor.
- Marketplace voices.
