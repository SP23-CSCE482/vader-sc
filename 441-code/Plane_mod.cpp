#include "Plane.h"


// Generated: Constructor, initializes parameters
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

// Generated: Destructor. This is the destructor for a plane.
Plane::~Plane()
{
}

// Generated: Intersect with a plane with a direction and a ray origin.
Intersection Plane::intersect(glm::vec3 raydirection, glm::vec3 rayorigin){
	return(Intersection{ (glm::dot((center - rayorigin), normal)) / (glm::dot(raydirection, normal)), this, true });
}

// Generated: Get the normal that is the intersection point of this plane.
glm::vec3 Plane::getNormal(glm::vec3 intersectionPoint) {
	return(glm::normalize(this->normal));
}

// Generated: Get the plane's velocity.
glm::vec3 Plane::getka(){
	return(this->ka);
}

// Generated: Get the K-position.
glm::vec3 Plane::getkd() {
	return(this->kd);
}

// Generated: Get the plane's current working vector.
glm::vec3 Plane::getks() {
	return(this->ks);
}

// Generated: Get the KM vector for this plane.
glm::vec3 Plane::getkm() {
	return(this->km);
}

// Generated: Get the n-coordinate of the plane.
float Plane::getn() {
	return(this->n);
}

// Generated: Get max extent of the plane.
Extent Plane::getMaxExtent()
{
	return this->maxExtent;
}

// Generated: get the average position of all planes
glm::vec3 Plane::getAveragePosition()
{
	return center; //there is no good way to do this with planes. planes should not be in the BVH
}
