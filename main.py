import openai

import tkinter as tk

from tkinter import messagebox

from tkinter import font




openai.api_key = "APİ-KEY"  



class QuestionGenerator:

    def __init__(self):

        self.questions = set()

        self.answers = set()



    def create_unique_question(self, metin):

        while True:

            prompt = (

                f"Verilen metinden '{metin}' kelimesiyle ilgili bir soru ve dört şık oluşturun. "

                f"Şıkların içerisinde doğru cevap da bulunmalıdır. Sadece doğru cevabı belirt."

            )



            try:

                response = openai.ChatCompletion.create(

                    model="gpt-3.5-turbo",

                    messages=[

                        {"role": "system", "content": "Sen bir yardımcısın."},

                        {"role": "user", "content": prompt}

                    ],

                    max_tokens=150

                )



                content = response['choices'][0]['message']['content']

                lines = content.strip().split('\n')

                soru = lines[0].strip()

                siklar = [line.strip() for line in lines[1:] if line.strip() != '' and len(line.strip().split()) > 1]



                if soru not in self.questions and all(sik not in self.answers for sik in siklar):

                    self.questions.add(soru)

                    for sik in siklar:

                        if sik.startswith("Doğru cevap"):

                            self.answers.add(sik.split(": ")[1])

                        else:

                            self.answers.add(sik.split(": ")[0])

                    return soru, siklar

                else:

                    continue



            except Exception as e:

                messagebox.showerror("Error", f"Hata: {str(e)}")

                return None, None



def generate_questions(metin, soru_sayisi):

    question_gen = QuestionGenerator()

    output_text.delete(1.0, tk.END)  

    for i in range(soru_sayisi):

        soru, siklar = question_gen.create_unique_question(metin)

        if soru and siklar:

            output_text.insert(tk.END, f"{i+1}. Soru: {soru}\n")

            output_text.insert(tk.END, f"Şıklar: {', '.join(siklar)}\n\n")

        else:

            break



def on_generate_button_click():

    metin = metin_entry.get()

    try:

        soru_sayisi = int(soru_sayisi_entry.get())

        generate_questions(metin, soru_sayisi)

    except ValueError:

        messagebox.showerror("Input Error", "Lütfen geçerli bir soru sayısı giriniz.")




def create_gui():

    global metin_entry, soru_sayisi_entry, output_text



    root = tk.Tk()

    root.title("Soru ve Şıklar Oluşturucu")

    root.configure(bg="#fafafa") 



    default_font = font.nametofont("TkDefaultFont")

    default_font.configure(size=11)



    frame = tk.Frame(root, bg="#fafafa")

    frame.pack(pady=10)



    tk.Label(frame, text="Metin:", bg="#fafafa", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)

    metin_entry = tk.Entry(frame, width=50, font=("Helvetica", 12))

    metin_entry.grid(row=0, column=1, padx=5, pady=10)



    tk.Label(frame, text="Soru Sayısı:", bg="#fafafa", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)

    soru_sayisi_entry = tk.Entry(frame, width=10, font=("Helvetica", 12))

    soru_sayisi_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")



    generate_btn = tk.Button(root, text="Soruları Oluştur", command=on_generate_button_click, bg="#4caf50", fg="#ffffff", font=("Helvetica", 12, "bold"))

    generate_btn.pack(pady=10)



    output_text = tk.Text(root, width=80, height=20, wrap="word", font=("Helvetica", 12))

    output_text.pack(pady=10)



    root.mainloop()



if __name__ == "__main__":

    create_gui()
