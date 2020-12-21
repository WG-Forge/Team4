#include "dijkstra_algo.h"
#include <algorithm>
#include <iostream>
#include <map>
#include <set>

//первая координата в тупле -- idx ребра, вторая -- его длина, затем идут смежные вершины
vector<pair<int, int>> GetOptimalPath(int begin_idx, int end_idx, const vector<tuple<int, int, pair<int, int>>> &gr) {
    map<int, vector<pair<int, int>>> graph;
    map<pair<int, int>, int> idx_edges;
    for (const auto &i : gr) {
        graph[get<2>(i).first].push_back({get<2>(i).second, get<1>(i)});
        graph[get<2>(i).second].push_back({get<2>(i).first, get<1>(i)});
        idx_edges[get<2>(i)] = get<0>(i);
    }
    map<int, int> parents, distance;
    map<int, bool> visited;
    for (const auto &item : graph) {
        distance.emplace(item.first, INT32_MAX);
        parents.emplace(item.first, 0);
        visited.emplace(item.first, false);
    }
    distance[begin_idx] = 0;

    set<pair<int, int>> q;
    q.insert({distance[begin_idx], begin_idx});
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());
        for (size_t j = 0; j < graph[v].size(); ++j) {
            int to = graph[v][j].first,
                len = graph[v][j].second;
            if (distance[v] + len < distance[to]) {
                q.erase(make_pair(distance[to], to));
                distance[to] = distance[v] + len;
                parents[to] = v;
                q.insert(make_pair(distance[to], to));
            }
        }
    }

    vector<int> path, orientation;
    vector<pair<int, int>> id_and_orient;
    for (int v = end_idx; v != begin_idx; v = parents[v]) {
        path.push_back(v);
    }
    path.push_back(begin_idx);
    reverse(path.begin(), path.end());
    for (size_t j = 0; j < path.size() - 1; j++) {
        if (idx_edges.count({path[j], path[j + 1]}) != 0) {
            id_and_orient.emplace_back(idx_edges[{path[j], path[j + 1]}], 1);
        } else {
            id_and_orient.emplace_back(idx_edges[{path[j+1], path[j]}], -1);
        }
    }

    return id_and_orient;
}

//int main() {
//    vector<tuple<int, int, pair<int, int>>> gr{{0, 7, {1, 2}}, {1, 9, {1, 3}}, {2, 10, {2, 3}}, {3, 14, {1, 6}}, {4, 2, {6, 3}}, {5, 9, {6, 5}}, {6, 6, {5, 4}}, {7, 11, {3, 4}}, {8, 15, {2, 4}}};
//    vector<pair<int, int>> path = GetOptimalPath(4, 6, gr);
//    for (const auto &i : path) {
//        cout << i.first << " " << i.second << "\n";
//    }
//
//    return 0;
//}
