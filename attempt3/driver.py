# file_path = "main.py"
# # num_times = 50  # Number of times to run the file

# # for _ in range(num_times):
# while True:
#     subprocess.call(["python", file_path])

import ai3
import copy
import multiprocessing
import training_module

if __name__ == '__main__':
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
    top100File = "object_file.pickle"
    top100List = ai3.load(top100File)

    
    num_processes = 5

# ---

    i = 10
    while i != 0:
        i -= 1

        trainingSet = []
        top100List = ai3.load(top100File)

        for model in top100List:
            model.score = 0
            trainingSet.append(model)
            for i in range(9):
                newModel = copy.deepcopy(model)
                newModel.mutate()
                trainingSet.append(newModel)
            model.generation += 1

        print(trainingSet[0].generation)

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(training_module.trainingInstance, split_list_into_even_lists(trainingSet, num_processes))

        trainingSet = [item for sublist in results for item in sublist]

        trainingSet.sort(key=lambda obj: obj.score, reverse=True)
        print(trainingSet[0].score, trainingSet[-1].score)
        ai3.export(top100File, trainingSet[:100])
        ai3.export(bestModelFile, trainingSet[0])
