#ifndef NEWPOSITION_NEWPOSITIONS_H
#define NEWPOSITION_NEWPOSITIONS_H

#include <iostream>
#include <vector>
#include <map>
#include <unordered_set>
#include <queue>
#include "math.h"

std::pair<double, double>
NewPosition(std::pair<double, double> cur_pos, const std::vector<std::pair<double, double>>& neighbours, double cool, double C);


#endif //NEWPOSITION_NEWPOSITIONS_H
