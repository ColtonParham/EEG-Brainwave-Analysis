import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data from the text file
df = pd.read_csv('Emotional.txt', delimiter=';')

# Plotting the data
plt.figure(figsize=(14, 8))
sns.lineplot(data=df, dashes=False)
plt.title('Data Visualization')
plt.xlabel('Index')
plt.ylabel('Values')
plt.legend(title='Series', loc='upper right')
plt.savefig('visualization.png')  # Save the plot as an image
