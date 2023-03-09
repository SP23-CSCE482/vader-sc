#pragma once
#include <vector>
#include "Shape.h"
#include "Light.h"
#include <GLM/glm.hpp>

class Scene
{
public:
	Scene(bool bunnymode);
	~Scene();
	glm::vec3 trace(glm::vec3 raydirection, glm::vec3 rayorigin, float t0, float t1, float depth);
	Intersection hit(glm::vec3 raydirection, glm::vec3 rayorigin, float t0, float t1);
	void pushShape(Shape* shape);
	void setBunnyMode(bool bunnyMode);


private:
	std::vector<Shape*> shapes;
	std::vector<Light*> lights;
	bool bunnymode = false;//bunnymode is false by default
};
