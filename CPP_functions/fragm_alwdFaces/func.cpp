#include "func.h"


std::vector<Fragment>
GetFragments(const std::vector<std::pair<int, int>> &graph, const std::vector<std::pair<int, int>> &subgraph) {
    std::unordered_set<int> subgraph_points;
    for (auto line : subgraph) {
        subgraph_points.insert(line.first);
        subgraph_points.insert(line.second);
    }
    std::unordered_map<int, bool> other_points;
    for (auto line : graph) {
        if (subgraph_points.find(line.first) == subgraph_points.end()) {
            other_points[line.first] = false;
        }
        if (subgraph_points.find(line.second) == subgraph_points.end()) {
            other_points[line.second] = false;
        }
    }
    std::vector<Fragment> fragments;
    Fragment fragment = {};
    for (auto &point : other_points) {
        if (!point.second) {
            std::queue<int> order;
            order.push(point.first);
            point.second = true;
            while (!order.empty()) {
                int cur = order.front();
                order.pop();
                if (std::find(fragment.main_points.begin(), fragment.main_points.end(), cur) ==
                    fragment.main_points.end() && subgraph_points.find(cur) != subgraph_points.end()) {
                    fragment.main_points.push_back(cur);
                }
                for (auto line : graph) {
                    if (line.first == cur || line.second == cur) {
                        int next_point = (cur == line.first) ? line.second : line.first;
                        if (subgraph_points.find(next_point) == subgraph_points.end() &&
                            !other_points[next_point]) {
                            order.push(next_point);
                            other_points[next_point] = true;
                        }
                        if ((other_points.find(next_point) != other_points.end() &&
                             other_points.find(cur) != other_points.end() &&
                             cur < next_point) ||
                            (subgraph_points.find(next_point) != subgraph_points.end()) ||
                            (subgraph_points.find(cur) != subgraph_points.end())) {
                            fragment.lines.emplace_back(next_point, cur);

                            if (std::find(fragment.main_points.begin(), fragment.main_points.end(), next_point) ==
                                fragment.main_points.end() &&
                                subgraph_points.find(next_point) != subgraph_points.end()) {
                                fragment.main_points.push_back(next_point);
                            }
                        }
                    }
                }
            }
            fragments.push_back(fragment);
            fragment = {};
        }
    }
    for (auto line : graph) {
        if (subgraph_points.find(line.first) != subgraph_points.end() &&
            subgraph_points.find(line.second) != subgraph_points.end() &&
            (std::find(std::begin(subgraph), std::end(subgraph), line) == std::end(subgraph) &&
             std::find(std::begin(subgraph), std::end(subgraph), std::make_pair(line.second, line.first)) ==
             std::end(subgraph))) {
            fragments.push_back({{line.first, line.second},
                                 {line}});
        }
    }
    return fragments;
}

std::vector<int> GetAllowedFace(std::vector<int> main_points, std::vector<std::vector<int>> faces) {
	std::vector<int> allowed_faces;
	std::sort(main_points.begin(), main_points.end());
	for (int i = 0; i < faces.size(); ++i) {
		std::vector<int> intersection;
		std::sort(faces[i].begin(), faces[i].end());
		std::set_intersection(faces[i].begin(), faces[i].end(), main_points.begin(), main_points.end(), std::back_inserter(intersection));
		if (intersection.size() == main_points.size()) {
			allowed_faces.push_back(i);
		}
	}
	return allowed_faces;
}