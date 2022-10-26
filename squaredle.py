import collections
from pyjsparser import parse
import requests
import json
from english_words import english_words_lower_alpha_set


class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.isWord = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for w in word:
            node = node.children[w]
        node.isWord = True

    def search(self, word):
        node = self.root
        for w in word:
            node = node.children.get(w)
            if not node:
                return False
        return node.isWord


def findWords(board, words):
    res = []
    trie = Trie()
    node = trie.root
    for w in words:
        trie.insert(w)
    for i in range(len(board)):
        for j in range(len(board[0])):
            dfs(board, node, i, j, "", res)
    return res


def dfs(board, node, i, j, path, res):
    if node.isWord and len(path) > 3:
        res.append(path)
        node.isWord = False
    if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
        return
    tmp = board[i][j]
    node = node.children.get(tmp)
    if not node:
        return
    board[i][j] = "#"
    dfs(board, node, i + 1, j, path + tmp, res)
    dfs(board, node, i - 1, j, path + tmp, res)
    dfs(board, node, i, j - 1, path + tmp, res)
    dfs(board, node, i, j + 1, path + tmp, res)
    dfs(board, node, i + 1, j + 1, path + tmp, res)
    dfs(board, node, i + 1, j - 1, path + tmp, res)
    dfs(board, node, i - 1, j + 1, path + tmp, res)
    dfs(board, node, i - 1, j - 1, path + tmp, res)
    board[i][j] = tmp


board = []
with open("script.json", "w") as outfile:
    json.dump(
        parse(requests.get("https://squaredle.app/api/today-puzzle-config.js").text),
        outfile,
    )
data = json.load(open("script.json", "r"))
# print(data["body"][0]["consequent"]["body"][2]["declarations"][0]["init"]["properties"][0]["value"]["properties"][0]["value"]["properties"][0]["value"]["elements"])
for i in data["body"][0]["consequent"]["body"][2]["declarations"][0]["init"][
    "properties"
][0]["value"]["properties"][0]["value"]["properties"][0]["value"]["elements"]:
    board.append([])
    for j in i["value"]:
        board[-1].append(str(j))

print(sorted(findWords(board, english_words_lower_alpha_set)))
