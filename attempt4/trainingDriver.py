import ai4
import trainingModule
import copy
import multiprocessing
import sys
import statistics

if __name__ == '__main__':
    num_processes = 1
    generations = float('inf')
    
    if len(sys.argv) > 1:
        num_processes = sys.argv[1]
        try:
            num_processes = int(num_processes)
        except:
            print("Invalid number of training instances.")
            exit()
    if len(sys.argv) > 2:
        generations = sys.argv[2]
        try:
            generations = int(generations)
        except:
            print("Invalid number of training generations.")
            exit()

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

# ---

    i = 0
    while i <= generations:
        i += 1

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

        print("-" * 20, f"Generation: {trainingSet[0].generation}", "-" * 20)

        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(trainingModule.trainingInstance, split_list_into_even_lists(trainingSet, num_processes))

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

        ai4.export(top100File, trainingSet[:100])
        ai4.export(bestModelFile, trainingSet[0])

