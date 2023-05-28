import ai4
import trainingModule
import copy
import multiprocessing

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
    top100File = "trainingModels.pickle"
    top100List = ai4.load(top100File)

    
    num_processes = 6

# ---

    i = 10
    while i != 0:
        i -= 1

        trainingSet = []
        top100List = ai4.load(top100File)

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
            results = pool.map(trainingModule.trainingInstance, split_list_into_even_lists(trainingSet, num_processes))

        trainingSet = [item for sublist in results for item in sublist]

        trainingSet.sort(key=lambda obj: obj.score, reverse=True)
        print(trainingSet[0].score, trainingSet[-1].score)
        ai4.export(top100File, trainingSet[:100])
        ai4.export(bestModelFile, trainingSet[0])

