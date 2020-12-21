//
// Created by Sofa on 13.11.2020.
//

#ifndef GETFRAGMENTS_FUNC_H
#define GETFRAGMENTS_FUNC_H

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <algorithm>


bool operator==(const std::pair<int, int> &lhs, const std::pair<int, int> &rhs);

struct Fragment {
    std::vector<int> main_points;
    std::vector<std::pair<int, int>> lines;
};

std::vector<Fragment>
GetFragments(const std::vector<std::pair<int, int>> &graph, const std::vector<std::pair<int, int>> &subgraph);

std::vector<int> GetAllowedFace(std::vector<int> main_points, std::vector<std::vector<int>> faces);

#endif //GETFRAGMENTS_FUNC_H
