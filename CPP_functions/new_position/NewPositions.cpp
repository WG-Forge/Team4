#include "NewPositions.h"

std::pair<double, double> NewPosition(
        int cur_vertex,
        const std::vector<std::pair<int, std::pair<double, double>>> &coordinates,
        const std::vector<std::pair<int, int>> &graph,
        const std::vector<int> &external_face,
        double cool,
        double A) {
    std::map<int, int> distances = CalculateDistances(graph, external_face);
    int max_per = 0;
    for (auto vertex : distances) {
        max_per = std::max(max_per, vertex.second);
    }
    std::unordered_map <int, std::pair<double, double>> index_to_coordinates;
    for (auto vertex : coordinates) {
        index_to_coordinates.insert(vertex);
    }
    std::pair<double, double> cur_force(0, 0);
    for (auto line : graph) {
        if (line.first == cur_vertex || line.second == cur_vertex) {
            int neighbour = (cur_vertex == line.first) ? line.second : line.first;
            double distance_x = index_to_coordinates[neighbour].first - index_to_coordinates[cur_vertex].first;
            double distance_y = index_to_coordinates[neighbour].second - index_to_coordinates[cur_vertex].second;
            double C = std::sqrt(distances.size() / 3.141592) * std::pow(2.718281, (2 * max_per
                                                                                    - distances[cur_vertex]
                                                                                    - distances[neighbour]) /
                                                                                   max_per * A);
            cur_force.first += C * distance_x * distance_x * distance_x;
            cur_force.second += C * distance_y * distance_y * distance_y;
        }
    }
    std::pair<double, double> new_position = index_to_coordinates[cur_vertex];
    new_position.first += std::min(static_cast<double>(cool), std::abs(cur_force.first)) *
                               (cur_force.first / std::abs(cur_force.first));
    new_position.second += std::min(static_cast<double>(cool), std::abs(cur_force.second)) *
                                cur_force.second / std::abs(cur_force.second);
    return new_position;
}


std::map<int, int> CalculateDistances(const std::vector<std::pair<int, int>> &graph,
                                      const std::vector<int> &external_face) {
    std::map<int, int> distances;
    std::unordered_set<int> vertexes(external_face.begin(), external_face.end());
    for (const auto &line : graph) {
        distances[line.first] = (vertexes.find(line.first) == vertexes.end()) ? -1 : 0;
        distances[line.second] = (vertexes.find(line.second) == vertexes.end()) ? -1 : 0;
    }
    std::queue<int> order;
    for (const auto& vertex : external_face) {
        order.push(vertex);
    }
    while (!order.empty()) {
        int cur = order.front();
        order.pop();
        for (auto line : graph) {
            if (line.first == cur || line.second == cur) {
                int next_point = (cur == line.first) ? line.second : line.first;
                if (distances[next_point] == -1) {
                    order.push(next_point);
                    distances[next_point] = distances[cur] + 1;
                }
            }
        }
    }
    return distances;
}