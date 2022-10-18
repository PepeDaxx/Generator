import tkinter
from tkinter import ttk, Tk, messagebox as mbox
from GarminScrapper import GarminScrapper
from Builder import Builder
scrapper = GarminScrapper()
builder = Builder()
file_path = 'source_code.json'
def download_source_code():
    try:
        scrapper.retreive_source_code(link=link.get(),file_path = file_path)

    except Exception as e:
        mbox.showerror('Błąd!',e)

def build_description():
    scrapped_data = scrapper.obtain_description_data(file_path)
    output_path = f'{scrapped_data["PN"]}.txt'
    builded_description = builder.build_description_from_dictionary(scrapped_data)
    with open (output_path,'w',encoding='UTF-8') as output_file:
        output_file.write(builded_description)
def build_table():
    scrapped_table = scrapper.obtain_table_data(file_path)
    output_path = f'{scrapped_table["PN"]}-table.txt'
    builded_table = builder.build_table(scrapped_table['TABLE'])
    with open (output_path,'w',encoding='UTF-8') as output_file:
        output_file.write(builded_table)

# Main Window
win = Tk()
win.title("Generator karty produktu")
# Main Label
label1 = ttk.Label(win, text="Link do produktu:").grid(column=0, row=0, columnspan=4)
# Link text area
link = tkinter.StringVar()
link_box = ttk.Entry(win, width=60, textvariable=link).grid(column=0, row=1)
# Buttons
download_button = ttk.Button(win, text="Pobierz dane", command=download_source_code).grid(column=1, row=1)
generate_button = ttk.Button(win, text="Wygeneruj opis", command=build_description).grid(column=2, row=1)
gen_table_button = ttk.Button(win, text="Wygeneruj tabelkę", command=build_table).grid(column=3, row=1)
win.mainloop()
