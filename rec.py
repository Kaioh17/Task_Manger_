# # def  search(nums, target, offset):
# #     # print(lst)
# #     # if not lst:
# #     #     return False
# #     # else:
# #         # mid = len(lst) // 2
# #         # if x == lst[mid]:
# #         #     return  True
# #         # elif x > lst[mid]:
# #         #     return bin_search(x, lst[mid + 1:])
# #         # elif x < lst[mid]:
# #         #     return bin_search(x, lst[:mid])
# #         if not nums:
# #             return -1
# #         else:
# #             mid = len(nums) // 2
# #
# #             if nums[mid] == target:
# #                 return offset + mid
# #             elif nums[mid] > target:
# #                 return search(nums[:mid], target, offset)
# #             elif nums[mid] < target:
# #                 return search(nums[mid + 1:], target, offset + mid + 1)
# #
# #
# # def fib(n):
# #     print(n)
# #     if n == 1:
# #         return 1
# #     elif n ==0:
# #         return 0
# #     else:
# #         print(n)
# #         return fib(n-1) + fib(n-2)
# #
# #
# # #
# # num = range(10)
# # print( search(list(num), 3, 0))
# # print(list(num[:5]))
# #
# # # print(fib(5))
#
# import tkinter as tk
# import time
#
# class TreeNode:
#     def __init__(self, val):
#         self.val = val
#         self.left = None
#         self.right = None
#
# class TreeVisualizer:
#     def __init__(self, root, x):
#         self.root = root
#         self.x = x
#         self.node_radius = 20
#         self.canvas_width = 800
#         self.canvas_height = 600
#         self.node_positions = {}
#         self.current_y = 50
#         self.animation_delay = 1000  # in milliseconds
#
#         self.window = tk.Tk()
#         self.window.title("Binary Tree Visualizer")
#         self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
#         self.canvas.pack()
#
#         self.count = 0
#         self.count_stack = []
#
#     def draw_tree(self):
#         def get_positions(node, depth, x_offset):
#             if node is None:
#                 return x_offset
#
#             x_offset = get_positions(node.left, depth + 1, x_offset)
#             self.node_positions[node] = (x_offset, depth * 100 + 50)
#             x_offset += 100
#             x_offset = get_positions(node.right, depth + 1, x_offset)
#             return x_offset
#
#         def draw_edges(node):
#             if node is None:
#                 return
#             x1, y1 = self.node_positions[node]
#             if node.left:
#                 x2, y2 = self.node_positions[node.left]
#                 self.canvas.create_line(x1, y1, x2, y2)
#                 draw_edges(node.left)
#             if node.right:
#                 x2, y2 = self.node_positions[node.right]
#                 self.canvas.create_line(x1, y1, x2, y2)
#                 draw_edges(node.right)
#
#         def draw_nodes():
#             for node, (x, y) in self.node_positions.items():
#                 self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill="lightblue")
#                 self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 12, "bold"))
#
#         get_positions(self.root, 0, 50)
#         draw_edges(self.root)
#         draw_nodes()
#
#     def highlight_node(self, node, color):
#         x, y = self.node_positions[node]
#         self.canvas.create_oval(x - self.node_radius, y - self.node_radius, x + self.node_radius, y + self.node_radius, fill=color)
#         self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 12, "bold"))
#         self.canvas.update()
#         self.canvas.after(self.animation_delay)
#
#     def show_count_step(self, val):
#         self.canvas.delete("count_text")
#         text = f"Current count: {val}"
#         self.canvas.create_text(self.canvas_width // 2, 20, text=text, font=("Arial", 16), tags="count_text")
#         self.canvas.update()
#
#     def count_less_than(self, node, x):
#         if node is None:
#             return 0
#
#         self.highlight_node(node, "yellow")
#
#         if x <= node.val:
#             result = self.count_less_than(node.left, x)
#             self.show_count_step(result)
#             return result
#         else:
#             left = self.count_less_than(node.left, x)
#             right = self.count_less_than(node.right, x)
#             result = 1 + left + right
#             self.show_count_step(result)
#             return result
#
#     def run(self):
#         self.draw_tree()
#         final_count = self.count_less_than(self.root, self.x)
#         self.canvas.create_text(self.canvas_width // 2, self.canvas_height - 30, text=f"Final count: {final_count}", font=("Arial", 16, "bold"), fill="green")
#         self.window.mainloop()
#
# # Helper to build BST from list
# def insert(root, val):
#     if not root:
#         return TreeNode(val)
#     if val < root.val:
#         root.left = insert(root.left, val)
#     else:
#         root.right = insert(root.right, val)
#     return root
#
# # Tree: [6, 3, 5, 4, 7, 1, 2, 9, 8, 0]
# values = [6, 3, 5, 4, 7, 1, 2, 9, 8, 0]
# root = None
# for val in values:
#     root = insert(root, val)
#
# visualizer = TreeVisualizer(root, x=6)
# visualizer.run()




"""Problem: Count Uni-value Subtrees

A uni-value subtree means all nodes of the subtree have the same value.

Task:
Given the root of a binary tree, write a function to count the number of uni-value subtrees.

Each leaf node is considered a uni-value subtree."""

#     5
#    / \
#   1   5
#  / \   \
# 5   5   5
class BSTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def __init__(self):
        self.size = 0
        self.root = None
#biggest problem is keeping count of values after
    def count_uni_value(self):
        def count(n):
            if not n:
                return 0
            elif not n.left or not n.right:
                return 1
            elif n.right == n:
                return count(n.right)
            elif n.left == n:
                return count(n.left) + 1
            elif n.right == n and n.left == n:
                return count(n.left) + count(n.right) + 1

        return count(self.root)