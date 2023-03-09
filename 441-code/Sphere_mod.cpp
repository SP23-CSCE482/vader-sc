#include "Sphere.h"
#include <iostream>

// Generated: Constructor for sphere
Sphere::Sphere(glm::vec3 position, float radius, glm::vec3 ka, glm::vec3 kd, glm::vec3 ks, glm::vec3 km, float n)
{
	this->position = position;
	this->radius = radius;
	this->ka = ka;
	this->kd = kd;
	this->ks = ks;
	this->km = km;
	this->n = n;

	//calculate maximum extent
	float minx = position[0] - radius;
	float miny = position[1] - radius;
	float minz = position[2] - radius;

	float maxx = position[0] + radius;
	float maxy = position[1] + radius;
	float maxz = position[2] + radius;
	this->maxExtent = Extent{ glm::vec3(minx, miny, minz), glm::vec3(maxx, maxy, maxz) };

}

// Generated: Destructor. This is the destructor for a sphere.
Sphere::~Sphere()
{
}

// Generated: Intersect with the sphere.
Intersection Sphere::intersect(glm::vec3 raydirection, glm::vec3 rayorigin) {
	float a = 1;
	float b = 2 * glm::dot(rayorigin - this->position, raydirection);
	float c = glm::dot(rayorigin - this->position, rayorigin - this->position) - this->radius * this->radius;
	
	float determinant = b * b - 4 * a * c;
	if (determinant < 0) {
		return(Intersection{ -1,this, false }); //return -1 because ray does not intersect
	}
	else {
		float lowt = (-b - glm::sqrt(determinant)) / (2 * a);
		float hight = (-b + glm::sqrt(determinant)) / (2 * a);
		if (lowt >= 0) {
			return(Intersection{ lowt, this, true });
		}
		else if(hight >= 0) {
			return(Intersection{ hight, this, true });
		}
		else {
			return(Intersection{ hight, this, false });
		}
	}
}

// Generated: Get the normal of the intersection point.
glm::vec3 Sphere::getNormal(glm::vec3 intersectionPoint) {
	return(glm::normalize(intersectionPoint - this->position));
}

// Generated: Get the ka vector for this sphere.
glm::vec3 Sphere::getka() {
	return(this->ka);
}

// Generated: Get the K-d vector for this sphere.
glm::vec3 Sphere::getkd() {
	return(this->kd);
}

// Generated: Get the sphere's knot vector.
glm::vec3 Sphere::getks() {
	return(this->ks);
}

// Generated: Get the mass of the sphere in km.
glm::vec3 Sphere::getkm() {
	return(this->km);
}

// Generated: Get the n coordinate of the sphere.
float Sphere::getn() {
	return(this->n);
}

// Generated: Get the maximum extent of the sphere.
Extent Sphere::getMaxExtent()
{
	return this->maxExtent;
}

// Generated: Get the average position of a sphere.
glm::vec3 Sphere::getAveragePosition()
{
	return position;//the average position of a sphere is just the position
}

