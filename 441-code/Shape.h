#pragma once
#include <GLM/glm.hpp>
#include "Light.h"

//Returning a struct makes it easier to deal with a BVH.


struct Extent {
	glm::vec3 minPoint;
	glm::vec3 maxPoint;
};

struct Intersection {
	float t;
	void* intersectedShape;
	bool didhit;
};

class Shape
{
public:
	Shape(void);
	~Shape(void);
	virtual Intersection intersect(glm::vec3 raydirection, glm::vec3 rayorigin) = 0;
	virtual glm::vec3 getNormal(glm::vec3 intersectionPoint) = 0;
	//intersect is a virtual function that every shape has to implement
	glm::vec3 shade(glm::vec3 raydirection, glm::vec3 rayorigin, glm::vec3 intersectionPoint, Light* light);
	virtual glm::vec3 getka() = 0;
	virtual glm::vec3 getkd() = 0;
	virtual glm::vec3 getks() = 0;
	virtual glm::vec3 getkm() = 0;
	virtual float getn() = 0;
	virtual Extent getMaxExtent() = 0;
	virtual void pushShape(Shape* shape) = 0;
	virtual void buildBVH() {};
	virtual glm::vec3 getAveragePosition() = 0;
	int depth = 0;
private:
	glm::vec3 ka;
	glm::vec3 kd;
	glm::vec3 ks;
	glm::vec3 km;
	Extent maxExtent;
	
};

