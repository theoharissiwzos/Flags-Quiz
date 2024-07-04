from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.clock import Clock
import random
import os

class FlagQuizScreen(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.score = 0
        self.time_left = 15  # Αρχικός χρόνος ανά ερώτηση σε δευτερόλεπτα
        self.flag_paths = self.load_flag_paths()
        self.used_flags = []  # Λίστα για τις σημαίες που έχουν ήδη εμφανιστεί
        self.current_flag = None
        self.timer = None
        
        # Προσθήκη εικόνας φόντου
        with self.canvas.before:
            self.background = Image(source='ret.png').texture  # Εισαγωγή φόντου
            self.rect = Rectangle(texture=self.background, pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

        # Κεντρικό layout
        center_box = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        
        # Ετικέτα τίτλου
        title_label = Label(text='Guess the Flag!', font_size='24sp', size_hint=(1, 0.2))
        
        # Κουμπί Play
        play_button = Button(text='Play', size_hint=(0.19, 0.04), pos_hint={'center_x': 0.5, 'y': 0.95})
        play_button.bind(on_press=self.start_game)
        
        # Προσθήκη ετικέτας τίτλου και κουμπιού στο κεντρικό layout
        center_box.add_widget(title_label)
        center_box.add_widget(play_button)
        
        # Προσθήκη του κεντρικού layout στην κύρια οθόνη
        self.add_widget(center_box)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def start_game(self, instance):
        self.clear_widgets()  # Εκκαθάριση όλων των widgets
        self.score = 0
        self.time_left = 15  # Αρχικός χρόνος ανά ερώτηση σε δευτερόλεπτα
        self.current_flag = None
        self.timer = None
        self.used_flags = []  # Επαναφορά της λίστας με τις εμφανισμένες σημαίες
        
        # Προσθήκη εικόνας φόντου
        with self.canvas.before:
            self.background = Image(source='wor.png').texture  # Εισαγωγή φόντου
            self.rect = Rectangle(texture=self.background, pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Ενημέρωση widgets για το παιχνίδι
        self.score_label = Label(text=f'Score: {self.score}', size_hint=(1, 0.1), color=[1, 1, 1, 1])
        self.timer_label = Label(text=f'Time: {self.time_left}', size_hint=(1, 0.1))
        self.user_guess = TextInput(hint_text='Enter country name', multiline=False, size_hint=(None, None), width=200, height=40, pos_hint={'right': 0.625})
        self.answer_button = Button(text='Check', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5})
        self.answer_button.bind(on_press=self.check_answer)
        self.flag_image = Image(size_hint=(1, 0.6))
        
        # Προσθήκη widgets στο layout
        self.add_widget(self.score_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.user_guess)
        self.add_widget(self.answer_button)
        self.add_widget(self.flag_image)
        
        Clock.schedule_once(self.initialize_quiz, 0)

    def initialize_quiz(self, dt):
        self.update_flag_and_score()  # Αρχική εμφάνιση σημαίας και ενημέρωση σκορ
        self.timer = Clock.schedule_interval(self.update_timer, 1)

    def update_flag_and_score(self):
        remaining_flags = [flag for flag in self.flag_paths if flag not in self.used_flags]
        if remaining_flags:
            self.current_flag = random.choice(remaining_flags)
            self.used_flags.append(self.current_flag)
            self.flag_image.source = self.current_flag
            self.flag_image.reload()
        else:
            self.return_to_menu()  # Επιστροφή στο μενού αφού ολοκληρωθούν όλες οι σημαίες
        
        self.time_left = 15  # Επαναφορά χρόνου ανά ερώτηση σε 10 δευτερόλεπτα
        self.timer_label.text = f'Time: {self.time_left}'  # Ενημέρωση ετικέτας χρόνου

    def load_flag_paths(self):
        flag_folder = 'flags'
        if not os.path.exists(flag_folder):
            os.makedirs(flag_folder)
        flag_files = [file for file in os.listdir(flag_folder) if file.endswith('.png')]
        return [os.path.join(flag_folder, file) for file in flag_files]

    def update_timer(self, dt):
        if self.current_flag:
            self.time_left -= 1
            self.timer_label.text = f'Time: {self.time_left}'
            if self.time_left <= 0:
                self.timer.cancel()
                self.timer_label.text = 'Time\'s up!'
                self.return_to_menu()  # Επιστροφή στο μενού αφού τελειώσει ο χρόνος

    def check_answer(self, instance):
        user_guess = self.user_guess.text.strip().lower()
        if not self.current_flag:
            return
        
        correct_country = os.path.basename(self.current_flag).split('.')[0]
        
        if user_guess == correct_country.lower():
            self.score += 1
            self.score_label.text = f'Score: {self.score}/195'  # Ενημέρωση ετικέτας βαθμολογίας
            self.score_label.color = [0, 1, 0, 1]  # Πράσινο χρώμα για σωστή απάντηση
            self.show_feedback("Correct!")
            self.user_guess.text = ''  # Καθαρισμός εισαγωγής κειμένου
            self.update_flag_and_score()  # Αλλαγή της σημαίας και ενημέρωση του σκορ
            
            # Έλεγχος αν έχουν τελειώσει όλες οι σημαίες και υπάρχει ακόμα χρόνος
            remaining_flags = [flag for flag in self.flag_paths if flag not in self.used_flags]
            if not remaining_flags and self.time_left > 0:
                self.show_feedback("Congratulations!")  # Εμφάνιση συγχαρητηρίων
        else:
            self.show_feedback("Wrong Answer!")
            self.score_label.text = f'Score: {self.score}/195'  # Ενημέρωση ετικέτας βαθμολογίας
            self.score_label.color = [1, 0, 0, 1]  # Κόκκινο χρώμα για λανθασμένη απάντηση

    def show_feedback(self, text):
        feedback_label = Label(text=text, font_size='24sp', size_hint=(1, 0.2), color=[1, 1, 1, 1])
        self.add_widget(feedback_label)
        Clock.schedule_once(lambda dt: self.remove_widget(feedback_label), 2)

    def return_to_menu(self, *args):
        self.clear_widgets()  # Αφαίρεση όλων των widgets
        self.add_widget(BoxLayout(orientation='vertical'))  # Προσθήκη νέου κεντρικού layout
        
        # Έλεγχος αν έχουν τελειώσει όλες οι σημαίες και αν υπάρχει ακόμα χρόνος
        remaining_flags = [flag for flag in self.flag_paths if flag not in self.used_flags]
        if remaining_flags and self.time_left <= 0:
            message_label = Label(text="Unfortunately, you lost. Please press the button below to restart the game.",
                                 font_size='18sp', size_hint=(1, 0.5), color=[1, 1, 1, 1])
        else:
            message_label = Label(text="Congratulations! You guessed all flags correctly. Press the button below to restart the game.",
                                 font_size='18sp', size_hint=(1, 0.5), color=[1, 1, 1, 1])
        
        # Κουμπί επιστροφής στο μενού
        menu_button = Button(text='Restart', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'y': 0.9})
        menu_button.bind(on_press=self.start_game)  # Σύνδεση με τη συνάρτηση εκκίνησης παιχνιδιού
        
        # Προσθήκη μηνύματος και κουμπιού στο layout
        self.add_widget(message_label)
        self.add_widget(menu_button)

class FlagQuizApp(App):

    def build(self):
        return FlagQuizScreen()

if __name__ == '__main__':
    FlagQuizApp().run()