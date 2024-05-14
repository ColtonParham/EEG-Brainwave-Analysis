import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the text file
df = pd.read_csv('Emotional.txt', delimiter=';')

# Setting up the plot
plt.figure(figsize=(14, 10))

# Plot each series in a separate subplot
fig, axs = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('Data Visualization')

# Plotting each series individually
series = ['O1', 'O2', 'T3', 'T4', 'O1_T3', 'O2_T4']
for i, ax in enumerate(axs.flat):
    sns.lineplot(data=df, x=df.index, y=series[i], ax=ax)
    ax.set_title(series[i])
    ax.set_xlabel('Index')
    ax.set_ylabel('Values')

plt.tight_layout()
plt.subplots_adjust(top=0.95)  # Adjust the top to make room for the main title
plt.savefig('visualization_improved.png')
plt.show()
