from pathlib import Path
import numpy as np

def main():
    counter = 55300
    file = f"milestoneQTables/QtableAt{counter}.npy"
    filePath = Path(file)
    if filePath.exists():
        Qtable = np.load(file)
        print(Qtable)
    else:
        print("file does not exist")
if __name__ == "__main__":
    main()