import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculator:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1800x900')
        self.master.title("BMI Calculator")

        # Create and place widgets
        tk.Label(master, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(master, text="Height (cm):").grid(row=1, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)
        self.result_write = tk.Label(master, text="")
        self.result_write.grid(row=4, column=0, columnspan=2, pady=5)

        self.save_button = tk.Button(master, text="Save Data", command=self.save_data)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.view_history_button = tk.Button(master, text="View History", command=self.view_history)
        self.view_history_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.user_data = []  # List to store user data

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  
            bmi = weight / (height ** 2)
            self.result_label.config(text=f"Your BMI: {bmi:.2f}")
            self.weight_entry.delete(0, tk.END)  # Clear weight entry
            self.height_entry.delete(0, tk.END)  # Clear height entry

            # Visualize BMI result with different colors
            if bmi < 18.5:
                self.result_label.config(fg="blue")# Underweight
                self.result_write.config(text="You are Underweight, Eat More!!")
                self.result_write.config(fg="blue")
            elif 18.5 <= bmi < 24.9:
                self.result_label.config(fg="green")  # Normal weight
                self.result_write.config(text="You are prefectly balanced")
                self.result_write.config(fg="green")
            elif 25 <= bmi < 29.9:
                self.result_label.config(fg="orange")  # Overweight
                self.result_write.config(text="You are Overweight, Do workout!!")
                self.result_write.config(fg="orange")
            else:
                self.result_label.config(fg="red")  # Obesity
                self.result_write.config(text="Hey! You need to go on a diet, You obese")
                self.result_write.config(fg="red")
            # Save the calculated BMI along with user input
            self.user_data.append({"Weight": weight, "Height": height, "BMI": bmi})
        except ValueError as e:
            self.result_label.config(text=f"Error: {str(e)}")
           

    def save_data(self):
        if self.user_data:
            messagebox.showinfo("Data Saved", "BMI data saved successfully.")
        else:
            messagebox.showwarning("No Data", "No BMI data to save.")

    def view_history(self):
        if not self.user_data:
            messagebox.showwarning("No Data", "No BMI data to view.")
            return

        # Create a new window for history and trends
        history_window = tk.Toplevel(self.master)
        history_window.title("BMI History and Trends")

        # Display historical data in a listbox
        history_listbox = tk.Listbox(history_window, width=40, height=10)
        history_listbox.pack(pady=10)

        for data in self.user_data:
            history_listbox.insert(tk.END, f"Weight: {data['Weight']} kg, Height: {data['Height']} cm, BMI: {data['BMI']:.2f}")

        # Create a button to show BMI trend analysis
        trend_button = tk.Button(history_window, text="Show BMI Trend", command=self.show_bmi_trend)
        trend_button.pack(pady=10)

    def show_bmi_trend(self):
        if not self.user_data:
            messagebox.showwarning("No Data", "No BMI data to analyze.")
            return

        weights = [data["Weight"] for data in self.user_data]
        heights = [data["Height"] for data in self.user_data]
        bmis = [data["BMI"] for data in self.user_data]

        # Plot BMI trend
        fig, axs = plt.subplots(3, 1, figsize=(8, 8))
        axs[0].plot(weights, label="Weight (kg)", marker='o')
        axs[0].set_title("Weight Trend")
        axs[0].set_xlabel("Data Points")
        axs[0].set_ylabel("Weight (kg)")
        axs[0].legend()

        axs[1].plot(heights, label="Height (cm)", marker='o', color='green')
        axs[1].set_title("Height Trend")
        axs[1].set_xlabel("Data Points")
        axs[1].set_ylabel("Height (cm)")
        axs[1].legend()

        axs[2].plot(bmis, label="BMI", marker='o', color='orange')
        axs[2].axhline(y=18.5, color='blue', linestyle='--', label="Underweight")
        axs[2].axhline(y=24.9, color='green', linestyle='--', label="Normal Weight")
        axs[2].axhline(y=29.9, color='red', linestyle='--', label="Overweight")
        axs[2].set_title("BMI Trend")
        axs[2].set_xlabel("Data Points")
        axs[2].set_ylabel("BMI")
        axs[2].legend()

        plt.tight_layout()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=600,y=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
