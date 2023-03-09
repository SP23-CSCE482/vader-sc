#include "Plane.h"


Plane::Plane(glm::vec3 center, glm::vec3 normal, glm::vec3 ka, glm::vec3 kd, glm::vec3 ks, glm::vec3 km, float n)
{
	this->center = center;
	this->normal = normal;
	this->ka = ka;
	this->kd = kd;
	this->ks = ks;
	this->km = km;
	this->n = n;
	//calculate maximum extent
	glm::vec3 minPoint = glm::vec3(std::numeric_limits<float>::min(),
		std::numeric_limits<float>::min(),
		std::numeric_limits<float>::min());
	glm::vec3 maxPoint = glm::vec3(std::numeric_limits<float>::max(),
		std::numeric_limits<float>::max(),
		std::numeric_limits<float>::max());
	this->maxExtent = Extent{ minPoint, maxPoint };
}

Plane::~Plane()
{
}

Intersection Plane::intersect(glm::vec3 raydirection, glm::vec3 rayorigin){
	return(Intersection{ (glm::dot((center - rayorigin), normal)) / (glm::dot(raydirection, normal)), this, true });
}

glm::vec3 Plane::getNormal(glm::vec3 intersectionPoint) {
	return(glm::normalize(this->normal));
}

glm::vec3 Plane::getka(){
	return(this->ka);
}

glm::vec3 Plane::getkd() {
	return(this->kd);
}

glm::vec3 Plane::getks() {
	return(this->ks);
}

glm::vec3 Plane::getkm() {
	return(this->km);
}

float Plane::getn() {
	return(this->n);
}

Extent Plane::getMaxExtent()
{
	return this->maxExtent;
}

glm::vec3 Plane::getAveragePosition()
{
	return center; //there is no good way to do this with planes. planes should not be in the BVH
}
