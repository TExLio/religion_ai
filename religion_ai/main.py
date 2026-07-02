import os
from kivy.config import Config

# 🚨 يجب أن يكون هذا السطر في البداية تماماً قبل استدعاء App أو أي ويدجيت
# نحدد اسم ملف الأيقونة التي ستضعها في نفس مجلد المشروع
Config.set('kivy', 'window_icon', 'system_icon.png')

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from ai_engine import ReligionAssistant

class StickyNotificationPopup(ModalView):
    def __init__(self, **kwargs):
        super(StickyNotificationPopup, self).__init__(**kwargs)
        self.size_hint = (0.98, 0.18)
        self.pos_hint = {'center_x': 0.5, 'y': 0.81}
        self.auto_dismiss = True 
        
        layout = BoxLayout(orientation='vertical', padding=4, spacing=2)
        self.assistant = ReligionAssistant('religion_data.json')
        
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=0.45, spacing=5)
        self.search_btn = Button(text="عرض", size_hint_x=0.2, background_color=(0.2, 0.2, 0.2, 1), font_size=12)
        self.search_btn.bind(on_press=self.perform_search)
        
        self.search_input = TextInput(hint_text="تنبيه نظام..", multiline=False, size_hint_x=0.8, halign="right", font_size=13)
        
        search_layout.add_widget(self.search_btn)
        search_layout.add_widget(self.search_input)
        layout.add_widget(search_layout)
        
        scroll_view = ScrollView(size_hint_y=0.55)
        self.result_label = Label(text="...", font_size=12, size_hint_y=None, halign="right", valign="top", color=(0.85, 0.85, 0.85, 1))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_label.bind(width=lambda im, text_width: setattr(self.result_label, 'text_size', (text_width, None)))
        
        scroll_view.add_widget(self.result_label)
        layout.add_widget(scroll_view)
        self.add_widget(layout)

    def perform_search(self, instance):
        query = self.search_input.text.strip()
        if query:
            response = self.assistant.search(query)
            self.result_label.text = response
            self.search_input.focus = False
        else:
            self.result_label.text = "⚠️ أدخل كلمة."

class ReligionApp(App):
    def build(self):
        # تحديد الأيقونة أيضاً داخل كائن التطبيق للتأكيد عند البناء للأندرويد
        self.icon = 'system_icon.png'
        popup = StickyNotificationPopup()
        popup.open()
        return BoxLayout()

if __name__ == '__main__':
    ReligionApp().run()