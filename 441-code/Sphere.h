#pragma once
#include "Shape.h"
#include <GLM/glm.hpp>

class Sphere :
	public Shape
{
public:
	Sphere(glm::vec3 position, float radius, glm::vec3 ka, glm::vec3 kd, glm::vec3 ks, glm::vec3 km, float n);
	~Sphere();
	Intersection intersect(glm::vec3 raydirection, glm::vec3 rayorigin);
	glm::vec3 getNormal(glm::vec3 intersectionPoint);
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
	glm::vec3 position;
	float radius;
	glm::vec3 ka;
	glm::vec3 kd;
	glm::vec3 ks;
	glm::vec3 km;
	float n;
	Extent maxExtent;
	
};
