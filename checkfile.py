# Function to read and display the contents of 'Emotional.txt'
def display_file_contents(filename):
    with open(filename, 'r') as file:
        contents = file.read()
    return contents

# Read and display the contents of the uploaded file
filename = '/workspaces/EEG-Brainwave-Analysis/Emotional.txt'
file_contents = display_file_contents(filename)
print("File contents:")
print(file_contents)
