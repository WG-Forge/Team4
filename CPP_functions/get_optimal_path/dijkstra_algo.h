#pragma once
#include <vector>
using namespace std;

vector<pair<int, int>> GetOptimalPath(int begin_idx, int end_idx, const vector<tuple<int, int, pair<int, int>>> &gr);

