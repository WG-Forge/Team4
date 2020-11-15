#include "find_alpha_path.h"
#include <algorithm>
#include <iostream>
#include <queue>
#include <unordered_map>
#include <unordered_set>

template<typename T, typename V>
bool Contain(T v, const unordered_map<T, V> &c) {
    return c.find(v) != c.end();
}

template<typename T>
bool Contain(const T &v, const vector<T> &vec) {
    return find(begin(vec), end(vec), v) != end(vec);
}

int dfs(int vertex, const unordered_map<int, vector<int>> &adjacency, vector<int> &parents, const vector<int> &points) {
    vector<bool> visited(adjacency.size());
    queue<int> que;
    que.push(vertex);
    visited[vertex] = true;
    parents[vertex] = -1;

    while (!que.empty()) {
        int v = que.front();
        que.pop();
        for (size_t i = 0; i < adjacency.at(v).size(); ++i) {
            int to = adjacency.at(v)[i];
            if (!visited[to] && !(Contain(to, points))) {
                visited[to] = true;
                que.push(to);
                parents[to] = v;
            } else if (Contain(to, points) && !visited[to]) {
                parents[to] = v;
                return to;
            }
        }
    }
    return -1;
}

vector<int> FindAlphaPath(const vector<pair<int, int>> &fragment, const vector<int> &points) {
    unordered_map<int, vector<int>> adjacency;
    for (const auto &line : fragment) {
        adjacency[line.first].push_back(line.second);
        adjacency[line.second].push_back(line.first);
    }
    vector<int> parents(adjacency.size());
    int last = 0;
    for (const auto &vertex : points) {
        if (Contain(vertex, adjacency)) {
            last = dfs(vertex, adjacency, parents, points);
            break;
        }
    }
    vector<int> cycle;
    for (; last != -1; last = parents[last]) {
        cycle.push_back(last);
    }
    return cycle;
}
//int main() {
//    //Пример применения
//
//    vector<pair<int, int>> p = {{0, 1}, {1, 2}, {2, 3}};
//    vector<int> subgraph = {0, 3};
//    vector<int> ans = FindAlphaPath(p, subgraph);
//    for (const auto &x : ans) {
//        cout << x << " ";//0 1 2 3
//    }
//    return 0;
//}
