import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import json
import sys
import statistics
import copy
import multiprocessing
import ai4
import trainingModule
import time

# Create a global variable to track the script execution state
running = False

# Function to start the script execution
def start_script():
    global running
    if running: return
    num_instances = int(num_instances_entry.get())
    running = True

    def split_list_into_even_lists(lst, x):
        # Calculate the size of each sub-list
        sublist_size = len(lst) // x
        remainder = len(lst) % x
        
        # Initialize the resulting list of sub-lists
        sublists = []
        
        # Split the original list into sub-lists
        start_index = 0
        for i in range(x):
            sublist_length = sublist_size + (1 if i < remainder else 0)
            end_index = start_index + sublist_length
            sublist = lst[start_index:end_index]
            sublists.append(sublist)
            start_index = end_index
        return sublists
    
    bestModelFile = "best_model.pickle"
    top100File = "trainingModels.pickle"
    top100List = ai4.load(top100File)

    while running:
        trainingSet = []
        top100List = ai4.load(top100File)

        for model in top100List:
            model.score = 0
            trainingSet.append(model)
            for _ in range(9):
                newModel = copy.deepcopy(model)
                newModel.mutate()
                trainingSet.append(newModel)
            model.generation += 1

        print("-" * 20, f"Generation: {trainingSet[0].generation}", "-" * 20)

        with multiprocessing.Pool(processes=num_instances) as pool:
            results = pool.map(trainingModule.trainingInstance, split_list_into_even_lists(trainingSet, num_instances))

        trainingSet = [item for sublist in results for item in sublist]
        trainingSet.sort(key=lambda obj: obj.score, reverse=True)
        scores = []
        for model in trainingSet: scores.append(model.score)

        print("Maximum:", scores[0])
        print("Minimum:", scores[-1])
        print("Average:", sum(scores) / len(scores))
        print("Mean:", statistics.mean(scores))
        print("Standard Deviation:", statistics.stdev(scores))

        top100Scores = scores[:100]
        print("\nTOP 100")
        print("Maximum:", top100Scores[0])
        print("Minimum:", top100Scores[-1])
        print("Average:", sum(top100Scores) / len(top100Scores))
        print("Mean:", statistics.mean(top100Scores))
        print("Standard Deviation:", statistics.stdev(top100Scores))

        with open('modelHistory.json', 'r') as file:
            json_data = json.load(file)

        # Step 2: Append data to the dictionary
        new_data = {trainingSet[0].generation: {
            "topMax": top100Scores[0],
            "topMin": top100Scores[-1],
            "topAvg": sum(top100Scores) / len(top100Scores),
            "topMean": statistics.mean(top100Scores),
            "topStdev": statistics.stdev(top100Scores),
            "Max": scores[0],
            "Min": scores[-1],
            "Avg": sum(scores) / len(scores),
            "Mean": statistics.mean(scores),
            "Stdev": statistics.stdev(scores)
        }}
        json_data.update(new_data)

        # Step 3: Write the updated dictionary back to the JSON file
        with open('modelHistory.json', 'w') as file:
            json.dump(json_data, file)

        ai4.export(top100File, trainingSet[:100])
        ai4.export(bestModelFile, trainingSet[0])

        plot_graph(currentGraph)

# Function to stop the script execution
def stop_script():
    global running
    running = False

# Redirect stdout to the text area
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

# Create the GUI
root = tk.Tk()
root.title("Script Controller")

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, padx=10, pady=10)

# Label and entry field for number of instances
num_instances_label = tk.Label(button_frame, text="Number of instances:")
num_instances_label.pack()

num_instances_entry = tk.Entry(button_frame)
num_instances_entry.pack(pady=5)

# Create buttons for starting and stopping the script
start_button = tk.Button(button_frame, text="Start Script", command=lambda: threading.Thread(target=start_script).start())
start_button.pack(pady=5)

stop_button = tk.Button(button_frame, text="Stop Script", command=stop_script)
stop_button.pack(pady=5)

# Create a frame to hold the graph and dropdown list
graph_frame = tk.Frame(root)
graph_frame.grid(row=0, column=1, padx=10, pady=10)

# Create a variable to store the graph canvas
graph_canvas = None
currentGraph = "topMax"

# Function to plot the graph
def plot_graph(plotCategory: str):
    global graph_canvas

    # Clear the existing graph if it exists
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()

    with open('modelHistory.json', 'r') as file:
        modelHistory = json.load(file)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    x = []
    y = []

    for generation in list(modelHistory):
        x.append(generation)
        y.append(modelHistory[generation][plotCategory])

    ax.plot(x, y)

    # Add a horizontal line at y = 0
    ax.axhline(y=0, color='k', linestyle='-')

    graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack()

# Dropdown list options
dropdown_options = [
    "topMax",
    "topMin",
    "topAvg",
    "topMean",
    "topStdev",
    "Max",
    "Min",
    "Avg",
    "Mean",
    "Stdev"
]

# Variable to store the selected option
selected_option = tk.StringVar(root)
selected_option.set(dropdown_options[0])

# Function to handle option selection
def handle_option_selection(event):
    currentGraph = event
    plot_graph(currentGraph)

# Dropdown list widget
dropdown_menu = tk.OptionMenu(graph_frame, selected_option, *dropdown_options, command=handle_option_selection)
dropdown_menu.pack(pady=5)

if graph_canvas == None: plot_graph(currentGraph)

# Create a frame to hold the stdout area
stdout_frame = tk.Frame(root)
stdout_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a scrolled text area for stdout
stdout_text = scrolledtext.ScrolledText(stdout_frame, height=20)
stdout_text.pack()

# Redirect stdout to the text area
sys.stdout = StdoutRedirector(stdout_text)

# Run the GUI event loop
root.mainloop()
