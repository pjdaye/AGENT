"""Pretty-prints a confusion matrix."""


def print_cm(cm, labels):
    """ Pretty-prints a confusion matrix.

    :param cm: The confusion matrix.
    :param labels: A list of labels to map classification indices to human-readable labels.
    """

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
            print(cell, end=" ")
        print()

    print()
