#include "Light.h"
#include "GLM/glm.hpp"

// Generated: Constructs a new light with the given position and color.
Light::Light(glm::vec3 position, glm::vec3 color){
	this->position = position;
	this->color = color;
}

// Generated: Destructor for the light object.
Light::~Light(void)
{
}
