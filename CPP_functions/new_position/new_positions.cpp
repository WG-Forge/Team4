#include "new_positions.h"

std::pair<double, double>
NewPosition(std::pair<double, double> cur_pos, const std::vector<std::pair<double, double>>& neighbours, double cool, double C) {
	std::pair<double, double> cur_force(0, 0);
	for (auto neighbour : neighbours) {
		double distance_x = neighbour.first - cur_pos.first;
		double distance_y = neighbour.second - cur_pos.second;
		cur_force.first += C * distance_x * distance_x * distance_x;
		cur_force.second += C * distance_y * distance_y * distance_y;
	}
	int coef = 1;
	if (cur_force.first < 0) coef = -1;
	cur_pos.first += std::min(cool, std::abs(cur_force.first)) * coef;
	coef = 1;
	if (cur_force.second < 0) coef = -1;
	cur_pos.second += std::min(cool, std::abs(cur_force.second)) * coef;
	return cur_pos;
}
