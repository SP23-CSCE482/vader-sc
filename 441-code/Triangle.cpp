#include "Triangle.h"


Triangle::Triangle(
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
	float n){
	this->n1 = n1;
	this->n2 = n2;
	this->n3 = n3;
	this->v1 = v1;
	this->v2 = v2;
	this->v3 = v3;
	this->ka = ka;
	this->kd = kd;
	this->ks = ks;
	this->km = km;
	this->n = n;
	float minx = glm::min(glm::min(v1[0],v2[0]),v3[0]);
	float miny = glm::min(glm::min(v1[1], v2[1]), v3[1]);
	float minz = glm::min(glm::min(v1[2], v2[2]), v3[2]);

	float maxx = glm::max(glm::max(v1[0], v2[0]), v3[0]);
	float maxy = glm::max(glm::max(v1[1], v2[1]), v3[1]);
	float maxz = glm::max(glm::max(v1[2], v2[2]), v3[2]);
	this->maxExtent = Extent{ glm::vec3(minx, miny, minz), glm::vec3(maxx, maxy, maxz) };
	//calculate maximum extent;
}

Triangle::~Triangle()
{
}

Intersection Triangle::intersect(glm::vec3 raydirection, glm::vec3 rayorigin){
	glm::vec3 E1 = v2 - v1;
	glm::vec3 E2 = v3 - v1;
	glm::vec3 S = rayorigin - v1;
	glm::vec3 S1 = glm::cross(raydirection, E2);
	glm::vec3 S2 = glm::cross(S, E1);

	glm::vec3 result = (1.0f / glm::dot(S1, E1)) * glm::vec3(glm::dot(S2,E2),glm::dot(S1,S),glm::dot(S2,raydirection));
	float t = result[0];
	float b1 = result[1];
	float b2 = result[2];

	//barycentric condition
	if (b1 >= 0 && b1 <= 1 && b2 >= 0 && b2 <= 1 && (b1 + b2) <= 1 && t >=0) {
		return(Intersection{ t,this, true });
	}
	else {
		return(Intersection{ -1, this, false });
	}

}

glm::vec3 Triangle::getNormal(glm::vec3 intersectionPoint) {
	glm::vec3 rayorigin = intersectionPoint;
	glm::vec3 raydirection = intersectionPoint + glm::vec3(0.1f, 0.1f, 0.1f);
	
	glm::vec3 E1 = v2 - v1;
	glm::vec3 E2 = v3 - v1;
	glm::vec3 S = rayorigin - v1;
	glm::vec3 S1 = glm::cross(raydirection, E2);
	glm::vec3 S2 = glm::cross(S, E1);

	glm::vec3 result = (1.0f / glm::dot(S1, E1)) * glm::vec3(glm::dot(S2, E2), glm::dot(S1, S), glm::dot(S2, raydirection));
	float t = result[0];
	float b1 = result[1];
	float b2 = result[2];
	float b3 = 1.0f - b1 - b2;
	return(b3 * n1 + b1 * n2 + b2 * n3); //barycentric coordinates are out of order
	//learned through trial and error which combination was the correct order
}

glm::vec3 Triangle::getka(){
	return(this->ka);
}

glm::vec3 Triangle::getkd() {
	return(this->kd);
}

glm::vec3 Triangle::getks() {
	return(this->ks);
}

glm::vec3 Triangle::getkm() {
	return(this->km);
}

float Triangle::getn() {
	return(this->n);
}

Extent Triangle::getMaxExtent()
{
	return this->maxExtent;
}

glm::vec3 Triangle::getAveragePosition()
{
	return((v1 + v2 + v3) * (1 / 3.0f));
}
