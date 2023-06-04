# import ai4
# import matplotlib.pyplot as plt

# model = ai4.load("best_model.pickle")
# print(model)

# # Define the number of nodes in each layer
# input_nodes = 10
# hidden_nodes = 5
# output_nodes = 3

# # Create a figure and axis object
# fig, ax = plt.subplots()

# for layerID in model.


# # # Plot the nodes for each layer
# # ax.scatter([1] * input_nodes, range(input_nodes), color='blue', label='Input Layer')
# # ax.scatter([2] * hidden_nodes, range(hidden_nodes), color='orange', label='Hidden Layer')
# # ax.scatter([3] * output_nodes, range(output_nodes), color='green', label='Output Layer')

# # # Connect the nodes with lines
# # for i in range(input_nodes):
# #     for j in range(hidden_nodes):
# #         ax.plot([1, 2], [i, j], color='gray')
# # for j in range(hidden_nodes):
# #     for k in range(output_nodes):
# #         ax.plot([2, 3], [j, k], color='gray')

# # Set the axis labels and title
# ax.set_xlabel('Layer')
# ax.set_ylabel('Node')
# ax.set_title('Neural Network Architecture')

# # Set the legend
# ax.legend()

# # Remove the axis ticks
# ax.set_xticks([])
# ax.set_yticks([])

# # Show the plot
# plt.show()

import matplotlib.pyplot as plt

# Define the number of nodes in each layer
input_nodes = 10
hidden_nodes = 5
output_nodes = 3

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the nodes for each layer
ax.scatter([1] * input_nodes, range(input_nodes), color='blue', label='Input Layer')
ax.scatter([2] * hidden_nodes, range(hidden_nodes), color='orange', label='Hidden Layer')
ax.scatter([3] * output_nodes, range(output_nodes), color='green', label='Output Layer')

# Connect the nodes with lines and add weights as labels
weights = [[0.2, 0.4, 0.6, 0.8, 1.0],
           [0.1, 0.3, 0.5, 0.7, 0.9],
           [0.3, 0.6, 0.9]]
for i in range(input_nodes):
    for j in range(hidden_nodes):
        if j < len(weights[0]):
            ax.plot([1, 2], [i, j], color='gray')
            ax.text(1.1, (9*i + j) / 10, str(weights[0][j]), color='gray')
for j in range(hidden_nodes):
    for k in range(output_nodes):
        if k < len(weights[1]):
            ax.plot([2, 3], [j, k], color='gray')
            ax.text(2.1, (4*j + k) / 5, str(weights[1][k]), color='gray')

# Add biases as labels for each node
biases = [0.1, 0.3, 0.5, 0.2, 0.4, 0.6, 0.3, 0.6, 0.9]
for i, bias in enumerate(biases):
    layer = 1 if i < input_nodes else 2
    ax.text(layer, i, str(bias), ha='center', va='center')

# Set the axis labels and title
ax.set_xlabel('Layer')
ax.set_ylabel('Node')
ax.set_title('Neural Network Architecture')

# Set the legend
ax.legend()

# Remove the axis ticks
ax.set_xticks([])
ax.set_yticks([])

# Show the plot
plt.show()