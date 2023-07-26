from collections import defaultdict

def fp_growth(transactions, min_support):
  """
  This function implements the FP-Growth algorithm.

  Args:
    transactions: A list of transactions. Each transaction is a list of items.
    min_support: The minimum support threshold.

  Returns:
    A list of frequent itemsets. Each frequent itemset is a list of items.
  """

  # Create a FP-tree.
  fp_tree = FPTree(transactions)

  # Mine the FP-tree for frequent itemsets.
  frequent_itemsets = fp_tree.mine(min_support)

  return frequent_itemsets


class FPTree:
  """
  This class represents an FP-tree.

  Args:
    transactions: A list of transactions. Each transaction is a list of items.
  """

  def __init__(self, transactions):
    self.root = None
    self.header_table = defaultdict(int)
    self.transactions = transactions

  def add_transaction(self, transaction):
    for item in transaction:
      self.header_table[item] += 1

    if self.root is None:
      self.root = Node(item)
    else:
      self._add_item_to_tree(self.root, item)

  def _add_item_to_tree(self, node, item):
    if item not in node.children:
      node.children[item] = Node(item)

    node.children[item].count += 1

  def mine(self, min_support):
    frequent_itemsets = []

    # Mine the root node.
    frequent_itemsets.extend(self._mine_node(self.root, min_support))

    # Mine the children nodes.
    for child in self.root.children.values():
      frequent_itemsets.extend(self._mine_node(child, min_support))

    return frequent_itemsets

  def _mine_node(self, node, min_support):
    if node.count < min_support:
      return []

    # Create a frequent itemset with the node's item.
    frequent_itemset = [node.item]

    # Mine the children nodes.
    for child in node.children.values():
      frequent_itemset.extend(self._mine_node(child, min_support))

    return frequent_itemset


class Node:
  """
  This class represents a node in an FP-tree.

  Args:
    item: The item in the node.
  """

  def __init__(self, item):
    self.item = item
    self.count = 0
    self.children = {}