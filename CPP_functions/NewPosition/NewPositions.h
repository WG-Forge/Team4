#ifndef NEWPOSITION_NEWPOSITIONS_H
#define NEWPOSITION_NEWPOSITIONS_H

#include <iostream>
#include <vector>
#include <map>
#include <unordered_set>
#include <queue>
#include "math.h"

std::map<int, int> CalculateDistances(const std::vector<std::pair<int, int>> &graph,
                                      const std::vector<int> &external_face);


std::pair<double, double> NewPosition(
        std::pair<int, std::pair<double, double>> cur_vertex,
        const std::vector<std::pair<int, std::pair<double, double>>> &neighbours,
        const std::vector<std::pair<int, int>> &graph,
        const std::vector<int> &external_face,
        double cool,
        double A);


#endif //NEWPOSITION_NEWPOSITIONS_H
