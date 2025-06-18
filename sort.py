def sort_treeview(tree, col, reverse):

    data = [(tree.set(child, col), child) for child in tree.get_children('')]

    try:
        data.sort(key=lambda x: float(x[0]), reverse=reverse)
    except ValueError:
        data.sort(reverse=reverse)

    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))


def setup_sorting(tree):
    for col in tree['columns']:
        tree.heading(col, command=lambda c=col: sort_treeview(tree, c, False))