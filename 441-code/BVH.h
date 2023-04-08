#pragma once
#include "Shape.h"
#include <vector>
#include <GLM/glm.hpp>

class BVH :
	public Shape
{
public:
	BVH();
	~BVH();

	Intersection intersect(glm::vec3 raydirection, glm::vec3 rayorigin);
	glm::vec3 getNormal(glm::vec3 intersectionPoint); //I do not use getNormal with BVH
	Extent getMaxExtent();
	glm::vec3 getka();
	glm::vec3 getkd();
	glm::vec3 getks();
	glm::vec3 getkm();
	float getn();
	void pushShape(Shape* shape);
	void buildBVH();
	int depth = 0;
	glm::vec3 getAveragePosition();

private:
	void updateBounds(Shape* newShape); //update bounds of BVH when new shape is added
	glm::vec3 minPoint;
	glm::vec3 maxPoint;
	std::vector<Shape*> children;//children of BVH
	
};
