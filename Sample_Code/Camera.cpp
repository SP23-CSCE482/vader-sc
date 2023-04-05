#include "Camera.h"

//Destructor for the Camera Object
Camera::~Camera(){}

//Constructor for Camera Object
Camera::Camera(int resolutionWidth, int resolutionHeight){
	renderedImage = new float[resolutionWidth * resolutionHeight * 3];
	memset(renderedImage, 0, sizeof(float) * resolutionWidth * resolutionHeight * 3);
	this->resolutionWidth = resolutionWidth;
	this->resolutionHeight = resolutionHeight;
}

// Takes a picture of a scene using the Camera
void Camera::TakePicture(Scene *scene){
	glm::vec3 G = eye - lookat;
	glm::vec3 W = 1.0f / (length(G)) * G;
	glm::vec3 U = glm::cross(up, W) / (length(cross(up, W)));
	glm::vec3 V = glm::cross(W, U);

	float LY = 2.0f * tan(fovY / 2.0f) * focalDistance;
	float PW = LY / resolutionHeight;
	float LX = PW * resolutionWidth;
	glm::vec3 originalPlane = ((eye + normalize(lookat - eye)) * focalDistance) - ((LX / 2) * U) - ((LY / 2) * V);

	ray holderRay;
	int k;
	int j;
	for (j = 0; j < resolutionHeight; j++) {
		for (k = 0; k < resolutionWidth; k++) {
			// For each pixel, loop for interpolation of both color and ray
			holderRay.origin = eye;
			holderRay.direction = normalize((((V * PW) * static_cast<float>(j + 0.5) + ((U * PW) * static_cast<float>(k + 0.5)) + originalPlane)) - eye);
			glm::vec3 calcNewColor = scene->calculateRayColorPlusUltraStyle(0, INFINITY, holderRay);
			renderedImage[2 + (j * resolutionWidth + k) * 3] = calcNewColor[2]; // b
			renderedImage[1 + (j * resolutionWidth + k) * 3] = calcNewColor[1]; // g
			renderedImage[0 + (j * resolutionWidth + k) * 3] = calcNewColor[0]; // r
			scene->sceneCounter = 0;
		}
	}
}
