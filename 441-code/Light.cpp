#include "Light.h"
#include "GLM/glm.hpp"

Light::Light(glm::vec3 position, glm::vec3 color){
	this->position = position;
	this->color = color;
}

Light::~Light(void)
{
}
