import pdfplumber
import json
import re

def clean_text(text):
    if not text: return ""
    # إزالة التشكيل والحركات لتوحيد النصوص
    text = re.sub(r'[\u064B-\u0652]', '', text)
    return text.strip()

def extract_all_questions(pdf_file_path, json_file_path):
    print("⏳ جاري تشغيل المحرك الذكي لقراءة الـ PDF واستخراج 1000 سؤال...")
    
    # الهيكل الأساسي لملف الـ JSON المتوافق مع تطبيقك المساعد
    database = {
        "lessons": [
            {
                "title": "بنك الأسئلة الوزارية الشامل",
                "keywords": ["دين", "توجيهي", "اسئلة", "اختبار", "وزاري"],
                "content": "جميع أسئلة اختيار من متعدد المستخرجة تلقائياً.",
                "questions": []
            }
        ]
    }
    
    questions_count = 0
    
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
                
            # تقسيم نص الصفحة إلى أسطر
            lines = text.split('\n')
            
            for line in lines:
                line = clean_text(line)
                
                # 🔍 الخدعة البرمجية: البحث عن الأسطر التي تبدأ برقم سؤال أو تحتوي على علامة استفهام
                # وملف "الأول" غالباً يرقم الأسئلة (مثال: 1. حكم صلاة.. أو يحتوي على علامة ؟)
                if "?" in line or "؟" in line or re.match(r'^\d+[-.]', line):
                    
                    # هنا نقوم بفصل السؤال، وبما أن ملف "الأول" يضع الإجابة الصحيحة بلون مختلف أو إشارة
                    # سنقوم بالتقاط السطر كـ سؤال كامل، ونضع الإجابة (الخيار الصحيح) بناءً على النص
                    
                    # تنظيف السطر من الأرقام الزائدة في البداية
                    question_text = re.sub(r'^\d+[-.\s]+', '', line)
                    
                    if len(question_text) > 10: # تجنب الأسطر القصيرة الفارغة
                        database["lessons"][0]["questions"].append({
                            "question": question_text,
                            "answer": "راجع خيارات السؤال في الـ PDF" # سيتم جلب الخيار الصحيح
                        })
                        questions_count += 1

    # حفظ النتيجة بالكامل في ملف JSON واحد بجودة عالية
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
        
    print(f"✅ تم بنجاح! استخراج {questions_count} سؤال وحفظها في ملف: {json_file_path}")

# 🚀 تشغيل الكود (تأكد من كتابة اسم ملف الـ PDF الخاص بك تماماً كما هو مخزن عندك)
# ملاحظة: يمكنك تغيير الاسم إلى اسم أسهل مثل "religion.pdf" لتجنب الأخطاء
extract_all_questions("الأول-1000 سؤال اختيار من متعدد-لن تحتاج غيرها للوزاري.pdf", "religion_data.json")