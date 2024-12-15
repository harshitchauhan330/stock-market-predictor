# Author: [Your Name Here]
# Course: CIS 350
# Assignment: Program 2 - Stock Market Simulator with Enhanced Logging

class Node:
    def __init__(self, elem, parent=None, left=None, right=None):
        self.elem = elem
        self.parent = parent
        self.left = left
        self.right = right


class BinaryTree:
    def lastLeftDescendant(self, w):
        """Return the leftmost Node of the subtree rooted at w."""
        while w.left:
            w = w.left
        return w

    def firstRightAncestor(self, w):
        """Return the first ancestor x of w where w is in the right subtree of x."""
        while w.parent and w == w.parent.right:
            w = w.parent
        return w.parent


class CompleteBinaryTree(BinaryTree):
    def __init__(self):
        self.root = None
        self.last = None
        self.size = 0

    def getParentOfNewLastNode(self):
        """Return the node where the next insertion would occur."""
        if self.size == 0:
            return None
        path = bin(self.size + 1)[3:]  # Binary path representation to the node
        current = self.root
        for direction in path[:-1]:
            current = current.left if direction == '0' else current.right
        return current

    def getNewLastNode(self):
        """Return the new last node after the current last node is removed."""
        if self.size == 0:
            return None
        path = bin(self.size)[3:]
        current = self.root
        for direction in path[:-1]:
            current = current.left if direction == '0' else current.right
        return current

    def add(self, elem):
        """Insert a new node with elem."""
        new_node = Node(elem)
        if self.size == 0:
            self.root = new_node
            self.last = new_node
        else:
            parent = self.getParentOfNewLastNode()
            if not parent.left:
                parent.left = new_node
            else:
                parent.right = new_node
            new_node.parent = parent
            self.last = new_node
        self.size += 1
        return new_node

    def remove(self):
        """Remove the last node and return it."""
        if self.size == 0:
            return None
        removed = self.last
        if self.size == 1:
            self.root = None
            self.last = None
        else:
            parent = removed.parent
            if parent.right == self.last:
                parent.right = None
            else:
                parent.left = None
            self.last = self.getNewLastNode()
        self.size -= 1
        return removed


class Heap(CompleteBinaryTree):
    def insert(self, elem):
        """Insert elem and maintain heap order."""
        node = self.add(elem)
        self.upHeapBubbling(node)

    def min(self):
        """Return the minimum element."""
        return self.root.elem if self.root else None

    def removeMin(self):
        """Remove the minimum element and maintain heap order."""
        if self.size == 0:
            return None
        min_elem = self.root.elem
        if self.size == 1:
            self.root = None
            self.last = None
            self.size = 0
        else:
            self.root.elem = self.last.elem
            self.remove()
            self.downHeapBubbling(self.root)
        return min_elem

    def upHeapBubbling(self, node):
        """Ensure heap property from node to root."""
        while node.parent and node.parent.elem > node.elem:
            node.elem, node.parent.elem = node.parent.elem, node.elem
            node = node.parent

    def downHeapBubbling(self, node):
        """Ensure heap property from root to leaves."""
        while node:
            smallest = node
            if node.left and node.left.elem < smallest.elem:
                smallest = node.left
            if node.right and node.right.elem < smallest.elem:
                smallest = node.right
            if smallest == node:
                break
            node.elem, smallest.elem = smallest.elem, node.elem
            node = smallest


class StockMarketSimulator:
    def __init__(self):
        self.buy_heap = Heap()  # Buy limit orders
        self.sell_heap = Heap()  # Sell limit orders
        self.timestamp = 0

    def add_order(self, order_type, shares, price, trader_id):
        price = -price if order_type == "buy" else price
        elem = (price, self.timestamp, shares, trader_id)
        self.timestamp += 1
        if order_type == "buy":
            self.buy_heap.insert(elem)
        else:
            self.sell_heap.insert(elem)
        self.process_trades()

    def process_trades(self):
        while self.buy_heap.size > 0 and self.sell_heap.size > 0:
            buy = self.buy_heap.min()
            sell = self.sell_heap.min()

            if -buy[0] >= sell[0]:  # Match condition
                traded_shares = min(buy[2], sell[2])
                buy = (buy[0], buy[1], buy[2] - traded_shares, buy[3])
                sell = (sell[0], sell[1], sell[2] - traded_shares, sell[3])

                if buy[2] == 0:
                    self.buy_heap.removeMin()
                else:
                    self.buy_heap.root.elem = buy

                if sell[2] == 0:
                    self.sell_heap.removeMin()
                else:
                    self.sell_heap.root.elem = sell
            else:
                break

    def print_orders(self, order_type):
        print(f"*** {order_type.capitalize()} Limit Orders ***")
        heap = self.buy_heap if order_type == "buy" else self.sell_heap
        orders = self._collect_heap_elements(heap.root)
        for order in sorted(orders, key=lambda x: (x[0], x[1])):
            display_price = -order[0] if order_type == "buy" else order[0]
            print(f"({display_price:.2f},{order[1]}):({order[2]},{order[3]})")

    def _collect_heap_elements(self, node):
        """Recursively collect elements from the heap."""
        if node is None:
            return []
        return [node.elem] + self._collect_heap_elements(node.left) + self._collect_heap_elements(node.right)


def main():
    simulator = StockMarketSimulator()
    with open("input.txt", "r") as file:
        for line in file:
            parts = line.strip().split()
            print(line.strip())  # Log the command
            if parts[0] in {"buy", "sell"}:
                simulator.add_order(parts[0], int(parts[1]), float(parts[2]), int(parts[3]))
            elif parts[0] == "print":
                simulator.print_orders(parts[1])


if __name__ == "__main__":
    main()
