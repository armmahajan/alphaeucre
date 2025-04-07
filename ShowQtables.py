from pathlib import Path
import numpy as np
import pandas as pd

from openpyxl import Workbook


def main():
    counter = 00000
    file = f"milestoneQTables/QtableAt{counter}.npy"
    filePath = Path(file)
    if filePath.exists():
        Qtable = np.load(file)
        print(Qtable)
    else:
        print("file does not exist")
    save = False
    if save:
        with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
            for i in range(Qtable.shape[0]):
                df = pd.DataFrame(Qtable[i])
                df.to_excel(writer, sheet_name=f"Layer_{i}", index=False)
if __name__ == "__main__":
    main()