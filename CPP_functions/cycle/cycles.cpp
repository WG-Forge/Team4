#include "find_cycle.h"
#include <iostream>
#include <set>

//Вызываем в виде vector<int> cycle = FindMinCycle(lines);
//Необходимо передать в функцию множество ребер в виде пары точек.

//Чтобы работало с любой нумерацией вершин:
vector<int> MapFromBadIndexes(vector<pair<int, int>> &lines) {
  set<int> s;
  for (const auto &x : lines) {
    s.insert(x.first);
    s.insert(x.second);
  }
  vector<int> v;
  for (auto it = s.begin(); it != s.end(); ++it) {
    v.push_back(*it);
  }
  for (auto &x : lines) {
    for (size_t i = 0; i < v.size(); i++) {
      if (v[i] == x.first) {
        x.first = i;
      }
      if (v[i] == x.second) {
        x.second = i;
      }
    }
  }
  return v;
}

vector<int> MapToBadIndexes(vector<int> &cycle, const vector<int> &dict) {
  for (auto &x : cycle) {
    for (size_t i = 0; i < dict.size(); i++) {
      if (i == x) {
        x = dict[i];
        break;
      }
    }
  }
  return cycle;
}

bool dfs(int v,
         int &cycle_end,
         int &cycle_beg,
         vector<int> &parents,
         vector<int> &visited,
         vector<vector<int>> &graph) {
  visited[v] = 1;
  for (size_t i = 0; i < graph[v].size(); ++i) {
    if (graph[v][i] != parents[v]) {
      int to = graph[v][i];
      if (visited[to] == 0) {
        parents[to] = v;
        if (dfs(to, cycle_end, cycle_beg, parents, visited, graph)) { return true; }
      } else if (visited[to] == 1) {
        cycle_end = v;
        cycle_beg = to;
        return true;
      }
    }
  }
  visited[v] = 2;
  return false;
}

//Находим цикл.
vector<int> FindCycle(vector<pair<int, int>> &lines) {
  // Переводим список ребер в матрицу смежности.
  set<int> unique;
  for (auto x : lines) {
    unique.insert(x.first - 1);
    unique.insert(x.second - 1);
  }
  int n = unique.size();
  vector<int> dict = MapFromBadIndexes(lines);
  vector<vector<int>> graph(n, vector<int>());
  for (const auto &x : lines) {
    int a = x.first;
    int b = x.second;
    graph[a].push_back(b);
    graph[b].push_back(a);
  }

  vector<int> cycle;
  for (int i = 0; i < n; ++i) {
    vector<int> parents(n), visited(n);
    int cycle_end = -1, cycle_beg = -1;
    parents[i] = -1;
    if (dfs(i, cycle_end, cycle_beg, parents, visited, graph)) {
      if (cycle_beg != -1) {
        while (cycle_end != cycle_beg) {
          cycle.push_back(cycle_end);
          cycle_end = parents[cycle_end];
        }
        cycle.push_back(cycle_beg);
      }
      break;
    }
  }
  return MapToBadIndexes(cycle, dict);
}
int main() {
  //Примеры:
  vector<pair<int, int>> lines{{1, 2}, {1, 5}, {1, 4}, {2, 5}, {2, 6}, {2, 4}, {2, 3}, {3, 6}, {4, 5}, {4, 6}};
  vector<int> c = FindCycle(lines);
  for (const auto &x : c) {
    cout << x << " ";
  }

  vector<pair<int, int>> lines1{{11, 22}, {22, 10}, {10, 13}, {11, 13}};
  vector<int> c1 = FindCycle(lines1);
  for (const auto &x : c1) {
    cout << x << " ";
  }

  return 0;
}