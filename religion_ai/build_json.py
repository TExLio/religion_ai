import pdfplumber
import json
import re

def extract_from_religion_pdf(pdf_path, json_path):
    print("⏳ جاري فحص وتحليل ملف 'الأول' واستخراج الـ 1000 سؤال...")
    
    database = {
        "lessons": [
            {
                "title": "بنك أسئلة التربية الإسلامية الشامل",
                "keywords": ["دين", "توجيهي", "وزاري", "قران", "سنه", "بدر", "احد", "ميراث"],
                "content": "تجميع شامل لأسئلة الضع دائرة من كتاب الأول.",
                "questions": []
            }
        ]
    }
    
    question_count = 0
    current_question = None
    
    with pdfplumber.open(pdf_path) as pdf:
        # نبدأ القراءة من الصفحة 3 لتجاوز المقدمة والشهادات
        for page_num in range(2, len(pdf.pages)):
            text = pdf.pages[page_num].extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                
                # إزالة الحركات لتسهيل المطابقة لاحقاً
                line_clean = re.sub(r'[\u064B-\u0652]', '', line)
                
                # 🔍 التقاط السطر إذا كان يبدأ برقم سؤال (مثال: 12. ما حكم...) أو يحتوي على علامة استفهام
                if re.match(r'^\d+[\s.-]', line_clean) or "؟" in line_clean or "?" in line_clean:
                    # إذا كان هناك سؤال سابق لم تكتمل خياراته، نحفظه أولاً
                    if current_question:
                        database["lessons"][0]["questions"].append(current_question)
                        question_count += 1
                    
                    # تنظيف نص السؤال من الأرقام في البداية
                    clean_q = re.sub(r'^\d+[\s.-]+', '', line_clean)
                    current_question = {
                        "question": clean_q,
                        "answer": "راجع خيارات السؤال في الـ PDF" # سيتم استبدالها يدوياً أو تركها للبحث السريع
                    }
                
                # 🔍 التقاط الخيارات (أ، ب، ج، د) لدمجها مع السؤال لكي تظهر لك بالبحث
                elif current_question and any(opt in line_clean for opt in ["أ)", "ب)", "ج)", "د)", "أ-", "ب-"]):
                    current_question["question"] += f" [ {line_clean} ]"
                    
    # حفظ السؤال الأخير
    if current_question:
        database["lessons"][0]["questions"].append(current_question)
        question_count += 1

    # حفظ النتيجة في ملف JSON متناسق
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
        
    print(f"✅ تم بنجاح! تم استخراج {question_count} سؤال وتجهيز ملف: {json_path}")

# تشغيل الكود (تأكد من وجود ملف religion.pdf في نفس المجلد)
extract_from_religion_pdf("religion.pdf", "religion_data.json")