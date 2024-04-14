import tkinter as tk
from tkinter import messagebox

#Creating method that calculates hypotenuse based on entry labels
def calculate_hypotenuse():
    try:
        side_a = int(entry_a.get())
        side_b = int(entry_b.get())

        if side_a <= 0 or side_b <= 0:
            raise ValueError("Sides must be positive integers")
        hypotenuse = (side_a ** 2 + side_b ** 2) ** 0.5
        hypotenuse = round(hypotenuse,3)

        entry_c.config(state="normal")
        entry_c.delete(0, tk.END)
        entry_c.insert(0, str(hypotenuse))
        entry_c.config(state="readonly")

    except ValueError as e:
        messagebox.showerror("Error", "Must be Valid Integer")

#Creating Method that will Exit GUI
def exit():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Hypotenuse Calculator")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Creating labels
label_a = tk.Label(frame, text="Side A:")
label_a.grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(frame)
entry_a.grid(row=0, column=1, padx=5, pady=5)

label_b = tk.Label(frame, text="Side B:")
label_b.grid(row=1, column=0, padx=5, pady=5)
entry_b = tk.Entry(frame)
entry_b.grid(row=1, column=1, padx=5, pady=5)

#Creating read only label for hypotenuse
label_c = tk.Label(frame, text="Side C:")
label_c.grid(row=2, column=0, padx=5, pady=5)
entry_c = tk.Entry(frame, state="readonly", bg="light grey")
entry_c.grid(row=2, column=1, padx=5, pady=5)

# Creating calculate and exit buttons
calculate_button = tk.Button(frame, text="Calculate", command=calculate_hypotenuse)
calculate_button.grid(row=3, columnspan=3, padx=5, pady=5)
exit_button = tk.Button(frame, text="     Exit     ", command=exit)
exit_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)

# Run the main event loop
root.mainloop()
