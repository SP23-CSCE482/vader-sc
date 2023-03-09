#include "Shape.h"

// Generated: The shape constructor.
Shape::Shape(void)
{
}

// Generated: Destructor. This is the destructor for the shape class.
Shape::~Shape(void)
{
}

// Generated: Intersection point of the light.
glm::vec3 Shape::shade(glm::vec3 raydirection, glm::vec3 rayorigin, glm::vec3 intersectionPoint, Light* light) {
	glm::vec3 Ci = light->color;
	glm::vec3 li = glm::normalize(light->position - intersectionPoint);
	glm::vec3 N = this->getNormal(intersectionPoint);
	glm::vec3 ri = glm::normalize(2 * glm::dot(li, N)* N - li);
	glm::vec3 E = glm::normalize(rayorigin - intersectionPoint);
	glm::vec3 diffuse = getkd() * glm::max(0.0f,glm::dot(li,N));
	glm::vec3 specular = getks() * glm::pow( glm::max(0.0f,glm::dot(ri,E)),getn() );
	return(Ci * (diffuse + specular));
}

