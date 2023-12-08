from tkinter.messagebox import askyesno
import customtkinter

class App(customtkinter.CTk):
    # commands
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_list_amount(self, new_list_amount: str):
        new_list_amount_int = int(new_list_amount)
        # if creating more lists
        if self.lists < new_list_amount_int:
            # for each new list
            for i in range(self.lists, new_list_amount_int):
                # create new tab for list
                file_name = f"toDoList{str(i)}.txt"
                new_list_name = f"List {str(i + 1)}"
                self.tabview.add(new_list_name)
                # create new texbox
                self.textboxes[i] = customtkinter.CTkTextbox(self.tabview.tab(new_list_name))
                self.textboxes[i].pack(fill="both", expand=True)
                # empty variables so they dont stack from removing and adding tabs
                self.toDoLists[i] = []
                self.textboxes[i].delete('1.0', 'end')
                self.nums[i] = 0
                # create or open already existing list files and get text from them to an array
                file = open(file_name, "a")
                file = open(file_name, "r")
                for j in file:
                    newJ = j.replace("\n", "")
                    self.toDoLists[i].append(newJ)
                file.close()
                # get text from array to textbox
                for j in self.toDoLists[i]:
                    self.nums[i] += 1
                    self.textboxes[i].insert('insert', (self.nums[i],j))
                    self.textboxes[i].insert('insert', "\n")
                self.textboxes[i].configure(state='disabled')
                self.lists += 1
        # if removing lists
        if self.lists > new_list_amount_int:
            # for each list to remove
            for i in range(new_list_amount_int, self.lists):
                new_list_name = f"List {str(i + 1)}"
                self.tabview.delete(new_list_name)
                self.lists -= 1

    def clear_list(self):
        # if current list is empty do nothing
        if self.nums[int(self.tabview.get()[-1]) - 1] == 0:
            return 0
        if askyesno("Confirm choise", f"Are you sure you want to clear {self.tabview.get()}?"):
            selected_tab = int(self.tabview.get()[-1]) - 1
            file_name = f"toDoList{str(selected_tab)}.txt"
            # clear everything connected to tab that is open
            self.textboxes[selected_tab].configure(state='normal')
            file = open(file_name, "w")
            file.write("")
            file.close()
            self.toDoLists[selected_tab] = []
            self.textboxes[selected_tab].delete('1.0', 'end')
            self.nums[selected_tab] = 0
            self.textboxes[selected_tab].configure(state='disabled')
    
    def add_to_list(self):
        # if entry is empty do nothing
        if self.entry_add.get() == "":
            return 0
        selected_tab = int(self.tabview.get()[-1]) - 1
        file_name = f"toDoList{str(selected_tab)}.txt"
        self.textboxes[selected_tab].configure(state='normal')
        self.nums[selected_tab] += 1
        # add text from entry to textbox and array
        self.textboxes[selected_tab].insert('insert', (self.nums[selected_tab],self.entry_add.get()))
        self.toDoLists[selected_tab].append(self.entry_add.get())
        self.textboxes[selected_tab].insert('insert', "\n")
        # clear entry
        self.entry_add.delete(0, 'end')
        # rewrite file from newly changed array
        file = open(file_name, "w")
        file.write("")
        file.close()
        file = open(file_name, "a")
        for i in self.toDoLists[selected_tab]:
            file.write(f"{i}\n")
        file.close()
        self.textboxes[selected_tab].configure(state='disabled')
    
    def remove_from_list(self):
        # if entry is empty or the number is not on the list do nothing
        if self.entry_remove.get() == "" or int(self.entry_remove.get()) > self.nums[int(self.tabview.get()[-1]) - 1]:
            return 0
        selected_tab = int(self.tabview.get()[-1]) - 1
        file_name = f"toDoList{str(selected_tab)}.txt"
        self.textboxes[selected_tab].configure(state='normal')
        self.nums[selected_tab] -= 1
        # remove selected line from array -> clear entry and texbox
        self.toDoLists[selected_tab].pop(int(self.entry_remove.get()) - 1)
        self.entry_remove.delete(0, 'end')
        self.textboxes[selected_tab].delete('1.0', 'end')
        # rewrite textbox and file from newly changed array
        self.nums[selected_tab] = 0
        for i in self.toDoLists[selected_tab]:
            self.nums[selected_tab] += 1
            self.textboxes[selected_tab].insert('insert', (self.nums[selected_tab],i))
            self.textboxes[selected_tab].insert('insert', "\n")
        
        file = open(file_name, "w")
        file.write("")
        file.close()
        file = open(file_name, "a")
        for i in self.toDoLists[selected_tab]:
            file.write(f"{i}\n")
        file.close()
        self.textboxes[selected_tab].configure(state='disabled')
    
    # GUI
    def __init__(self):
        super().__init__()

        # configure window
        self.title("To do list")
        self.geometry(f"{900}x{640}")
        self.minsize(640, 640)

        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # create left side
        self.frame_sidebar = customtkinter.CTkFrame(self)
        self.frame_sidebar.grid(row=0, column=0, sticky="nsew")
        self.frame_sidebar.grid_rowconfigure(9, weight=1)
        
        self.label_add = customtkinter.CTkLabel(self.frame_sidebar, text="What do you want to add?", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_add.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.entry_add = customtkinter.CTkEntry(self.frame_sidebar, placeholder_text="shower")
        self.entry_add.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.button_add = customtkinter.CTkButton(self.frame_sidebar, text="add", font=customtkinter.CTkFont(size=15), command=self.add_to_list)
        self.button_add.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.label_remove = customtkinter.CTkLabel(self.frame_sidebar, text="Which one do you want to remove?", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_remove.grid(row=3, column=0, padx=20, pady=(30, 10))
        self.entry_remove = customtkinter.CTkEntry(self.frame_sidebar, placeholder_text="1")
        self.entry_remove.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.button_remove = customtkinter.CTkButton(self.frame_sidebar, text="remove", font=customtkinter.CTkFont(size=15), command=self.remove_from_list)
        self.button_remove.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.button_clear = customtkinter.CTkButton(self.frame_sidebar, text="clear current list", font=customtkinter.CTkFont(size=15), command=self.clear_list)
        self.button_clear.grid(row=6, column=0, padx=20, pady=(30 ,10), sticky="ew")
        
        self.label_lists = customtkinter.CTkLabel(self.frame_sidebar, text="Amount of lists", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_lists.grid(row=7, column=0, padx=20, pady=(30, 10))
        self.optionmenu_lists = customtkinter.CTkOptionMenu(self.frame_sidebar, values=["1", "2", "3", "4", "5"], font=customtkinter.CTkFont(size=15), command=self.change_list_amount)
        self.optionmenu_lists.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        self.label_appearance = customtkinter.CTkLabel(self.frame_sidebar, text="Appearance Mode:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_appearance.grid(row=10, column=0, padx=20, pady=(30, 10))
        self.optionmenu_appearance = customtkinter.CTkOptionMenu(self.frame_sidebar, values=["System", "Dark", "Light"], font=customtkinter.CTkFont(size=15), command=self.change_appearance_mode_event)
        self.optionmenu_appearance.grid(row=11, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # create right side
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.tabview.add("List 1")
        
        self.textboxes = [0, 0, 0, 0, 0]
        self.textboxes[0] = customtkinter.CTkTextbox(self.tabview.tab("List 1"))
        self.textboxes[0].pack(fill="both", expand=True)
        
        # create variables
        self.nums = [0, 0, 0, 0, 0]
        self.nums[0] = 0
        self.toDoLists = [0, 0, 0, 0, 0]
        self.toDoLists[0] = []
        self.lists = 1
        
        # create or open already existing list files and get text from them to an array
        file = open("toDoList0.txt", "a")
        file = open("toDoList0.txt", "r")
        for i in file:
            newI = i.replace("\n", "")
            self.toDoLists[0].append(newI)
        file.close()
        
        # get text from arrays to textbox
        for i in self.toDoLists[0]:
            self.nums[0] += 1
            self.textboxes[0].insert('insert', (self.nums[0],i))
            self.textboxes[0].insert('insert', "\n")
        
        # lock textbox after editing it
        self.textboxes[0].configure(state='disabled')
        
if __name__ == "__main__":
    app = App()
    app.mainloop()