#pragma once
#include "Shape.h"
#include <GLM/glm.hpp>

class Triangle :
	public Shape
{
public:
	Triangle(
		glm::vec3 n1,
		glm::vec3 n2,
		glm::vec3 n3,
		glm::vec3 v1,
		glm::vec3 v2,
		glm::vec3 v3,
		glm::vec3 ka,
		glm::vec3 kd,
		glm::vec3 ks,
		glm::vec3 km,
		float n);
	~Triangle();

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
	glm::vec3 n1;
	glm::vec3 n2;
	glm::vec3 n3;
	glm::vec3 v1;
	glm::vec3 v2;
	glm::vec3 v3;
	glm::vec3 ka;
	glm::vec3 kd;
	glm::vec3 ks;
	glm::vec3 km;
	float n;
	Extent maxExtent;
};
