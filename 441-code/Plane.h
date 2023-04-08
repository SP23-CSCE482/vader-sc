#pragma once
#include "Shape.h"
#include <GLM/glm.hpp>

class Plane :
	public Shape
{
public:
	Plane(glm::vec3 center, glm::vec3 normal, glm::vec3 ka, glm::vec3 kd, glm::vec3 ks, glm::vec3 km, float n);
	~Plane();

	Intersection intersect(glm::vec3 raydirection, glm::vec3 rayorigin);
	glm::vec3 getNormal(glm::vec3 intersectionPoint); //IP not needed for plane, but keeping method same for plane and sphere
	glm::vec3 getka();
	glm::vec3 getkd();
	glm::vec3 getks();
	glm::vec3 getkm();
	float getn();
	Extent getMaxExtent();
	void pushShape(Shape* shape) {};
	int depth = 0;
	glm::vec3 getAveragePosition();

private:
	glm::vec3 center;
	glm::vec3 normal;
	glm::vec3 ka;
	glm::vec3 kd;
	glm::vec3 ks;
	glm::vec3 km;
	Extent maxExtent;
	float n;
};
