#include "Camera.h"

#include <iostream>

// Generated: Destructor. This is the destructor.
// Generated: Destructor. This is the destructor.
Camera::~Camera()
{
}

// Generated: Construct a new camera with the given resolution.
// Generated: Construct a new camera with the given resolution.
Camera::Camera(int widthRes, int heightRes, glm::vec3 eye, glm::vec3 lookat, glm::vec3 up, float fovY, float focalDistance)
{
	this->widthRes = widthRes;
	this->heightRes = heightRes;
	this->eye = eye;
	this->lookat = lookat;
	this->up = up;
	this->FovY = fovY;
	this->focalDistance = focalDistance;
	renderedImage = new float[widthRes * heightRes * 3];
}



// Generated: Take the current picture.
// Generated: Take the current picture.
void Camera::TakePicture(Scene *scene)
{	
	memset(renderedImage, 0, sizeof(float) * widthRes * heightRes * 3);
	glm::vec3 w = glm::normalize(lookat-eye);
	glm::vec3 u = glm::normalize(glm::cross(w, up));
	glm::vec3 v = glm::cross(u,w);

	float ly = 2.0f * focalDistance * glm::tan(FovY / 2);
	float lx = ly * widthRes / heightRes;
	float pw = ly / heightRes;
	glm::vec3 origin = w * focalDistance - lx / 2.0f * u - ly / 2.0f * v + eye;

	std::cout << "origin: " << origin[0] << ", " << origin[1] << ", " << origin[2] << std::endl;
	std::cout << "eye: " << eye[0] << ", " << eye[1] << ", " << eye[2] << std::endl;
	std::cout << "w: " << w[0] << ", " << w[1] << ", " << w[2] << std::endl;
	std::cout << "u: " << u[0] << ", " << u[1] << ", " << u[2] << std::endl;
	std::cout << "v: " << v[0] << ", " << v[1] << ", " << v[2] << std::endl;
	std::cout << "ly: " << ly << std::endl;
	std::cout << "lx: " << lx << std::endl;
	std::cout << "pw: " << pw << std::endl;
	
	for (int y = 0; y < heightRes; y++) {
		for (int x = 0; x < widthRes; x++) {
			glm::vec3 pc = origin + pw * (x + 0.5f) * u + pw * (y + 0.5f) * v;
			glm::vec3 prd = glm::normalize(pc - eye);
			glm::vec3 color = scene->trace(prd, eye, 0, std::numeric_limits<float>::max(), 20);
			int index = 3 * (y * widthRes + x);
			renderedImage[index + 0] = color[0];
			renderedImage[index + 1] = color[1];
			renderedImage[index + 2] = color[2];
		}
	}	
}
