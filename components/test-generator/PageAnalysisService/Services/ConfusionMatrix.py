def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    print("Confusion Matrix")

    column_width = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * column_width

    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(column_width) % label, end=" ")
    print()

    for i, label1 in enumerate(labels):
        print("    %{0}s".format(column_width) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(column_width) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()

    print()


def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]
    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)
    return df