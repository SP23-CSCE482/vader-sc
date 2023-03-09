#pragma once
#include <vector>
#include "Scene.h"
#include <GLM/glm.hpp>


class Camera
{
public:
	~Camera();
	Camera(int widthRes, int heightRes, glm::vec3 eye, glm::vec3 lookat, glm::vec3 up, float fovY, float focalDistance);

	void TakePicture(Scene *scene);
	float* GetRenderedImage() { return renderedImage; };

private:

	int widthRes;
	int heightRes;
	glm::vec3 eye;
	glm::vec3 lookat;
	glm::vec3 up;
	float FovY;
	float focalDistance;

	float *renderedImage;


};
