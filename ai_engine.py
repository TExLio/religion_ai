import json
import re

class ReligionAssistant:
    def __init__(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            
    def clean_text(self, text):
        if not text: return ""
        text = re.sub(r'[\u064B-\u0652]', '', text) 
        text = re.sub(r'[أإآٱ]', 'ا', text)
        text = re.sub(r'[ة]', 'ه', text)
        text = re.sub(r'[ى]', 'ي', text)
        text = re.sub(r'\bال', '', text)
        return text.strip().lower()

    def search(self, user_query):
        cleaned_query = self.clean_text(user_query)
        if len(cleaned_query) < 2:
            return "⚠️ اكتب كلمة واضحة."
        
        results = []
        for lesson in self.data['lessons']:
            # البحث داخل الأسئلة مباشرة وعرض الأجوبة فوراً
            for qna in lesson['questions']:
                cleaned_question = self.clean_text(qna['question'])
                cleaned_answer = self.clean_text(qna['answer'])
                
                # إذا كانت الكلمة التي كتبتها موجودة بالسؤال أو بالجواب
                if cleaned_query in cleaned_question or cleaned_query in cleaned_answer:
                    results.append(f"• {qna['answer']}")
            
        if results:
            # دمج الأجوبة مباشرة تحت بعضها بدون أي نصوص إضافية أو أسماء دروس
            return "\n".join(results)
        
        return "❌ لا يوجد."
