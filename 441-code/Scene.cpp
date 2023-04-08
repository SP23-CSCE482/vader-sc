#include "Scene.h"
#include "Light.h"
#include "Plane.h"
#include "Shape.h"
#include "Sphere.h"

#include <iostream>
Scene::~Scene()
{
	for (size_t i = 0; i < this->shapes.size(); i++) {
		delete shapes.at(i);
	}
	for (size_t i = 0; i < this->lights.size(); i++) {
		delete lights.at(i);
	}
}

Scene::Scene(bool bunnymode)
{
	if(!bunnymode) {
		Shape* sphere1 = new Sphere(
			glm::vec3(-1.0f, -0.7f, 3.0f),
			0.3f,
			glm::vec3(0.1f, 0.1f, 0.1f),
			glm::vec3(0.2f, 1.0f, 0.2f),
			glm::vec3(1.0f, 1.0f, 1.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			100.0f);
		shapes.push_back(sphere1);

		Shape* sphere2 = new Sphere(
			glm::vec3(1.0f, -0.5f, 3.0f),
			0.5f,
			glm::vec3(0.1f, 0.1f, 0.1f),
			glm::vec3(0.0f, 0.0f, 1.0f),
			glm::vec3(1.0f, 1.0f, 1.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			10.0f);
		shapes.push_back(sphere2);

		Shape* sphere3 = new Sphere(
			glm::vec3(-1.0f, 0.0f, -0.0f),
			1.0f,
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(1.0f, 1.0f, 1.0f),
			0.0f);
		shapes.push_back(sphere3);

		Shape* sphere4 = new Sphere(
			glm::vec3(1.0f, 0.0f, -1.0f),
			1.0f,
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.8f, 0.8f, 0.8f),
			100.0f);
		shapes.push_back(sphere4);

		Shape* plane1 = new Plane(
			glm::vec3(0.0f, -1.0f, 0.0f),
			glm::vec3(0.0f, 1.0f, 0.0f),
			glm::vec3(0.1f, 0.1f, 0.1f),
			glm::vec3(1.0f, 1.0f, 1.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			0.0f);
		shapes.push_back(plane1);
		Shape* plane2 = new Plane(
			glm::vec3(0.0f, 0.0f, -3.0f),
			glm::vec3(0.0f, 0.0f, 1.0f),
			glm::vec3(0.1f, 0.1f, 0.1f),
			glm::vec3(1.0f, 1.0f, 1.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			glm::vec3(0.0f, 0.0f, 0.0f),
			0.0f);
		shapes.push_back(plane2);
	}
	//always have these lights
	Light* light1 = new Light(
		glm::vec3(0.0f, 3.0f, -2.0f),
		glm::vec3(0.2f, 0.2f, 0.2f));
	lights.push_back(light1);

	Light* light2 = new Light(
		glm::vec3(-2.0f, 1.0f, 4.0f),
		glm::vec3(0.5f, 0.5f, 0.5f));
	lights.push_back(light2);

	this->bunnymode = bunnymode;
}

void Scene::pushShape(Shape* shape) {
	shapes.push_back(shape);
}


//made hit a separate function so that shadow could use it as well
Intersection Scene::hit(glm::vec3 raydirection, glm::vec3 rayorigin, float t0, float t1) {
	float mint = std::numeric_limits<float>::max();
	Shape* bestshape = nullptr;
	bool didhit = false;
	glm::vec3 rayoriginp = rayorigin + (raydirection) * t0; //shoot ray from a point t0*raydirection away from rayorigin

	//find closest intersection
	for (Shape* shape : shapes) {
		Intersection intersection = shape->intersect(raydirection, rayoriginp);
		float intersectiontime = intersection.t + t0;//adjust intersectiontime by t0 since rayorigin was adjusted by t0
		if (intersectiontime < mint && intersectiontime >= t0 && intersectiontime <= t1) {
			bestshape = (Shape*)intersection.intersectedShape;
			mint = intersectiontime;
			didhit = true;
		}
	}
	Intersection output = { mint, bestshape, didhit };
	return(output);
}

glm::vec3 Scene::trace(glm::vec3 raydirection, glm::vec3 rayorigin, float t0, float t1, float depth) {
	Intersection rayhit = hit(raydirection, rayorigin, t0, t1);
	float mint = rayhit.t;
	Shape* bestshape = (Shape*)rayhit.intersectedShape;

	glm::vec3 Idirect;//direct lighting
	if (mint >= 0 && rayhit.didhit) {
		glm::vec3 color = glm::vec3(0.0f, 0.0f, 0.0f);
		color += bestshape->getka();
		glm::vec3 intersectionPoint = rayorigin + raydirection * mint; //get point of intersection from time - evaluate parametric equation

		for (Light* light : lights) {
			glm::vec3 lightdirection = glm::normalize(light->position - intersectionPoint);
			float lightdistance = glm::abs(glm::length(light->position - intersectionPoint));
			Intersection lighthit = hit(lightdirection, intersectionPoint, 0.001f, lightdistance+0.001f);
			float lightintersection = lighthit.t;
			Shape* hitshape = (Shape*)lighthit.intersectedShape;
			//the shape is at t=1 in reference to the light in this situation. so just make sure that the intersection is < epsilon
			//if the hit shape is the same shape
			if (!lighthit.didhit || lighthit.t >= lightdistance) {
				color += bestshape->shade(raydirection, rayorigin, intersectionPoint, light);
			}
		}
			
		Idirect = color;
	}
	else {
		Idirect = glm::vec3(0.0f, 0.0f, 0.0f);
	}

	if (depth > 1 && bestshape != nullptr) {
		glm::vec3 intersectionPoint = rayorigin + raydirection * mint;
		glm::vec3 N = bestshape->getNormal(intersectionPoint);
		glm::vec3 reflectedRay = glm::normalize(2 * glm::dot(glm::normalize(-raydirection), N) * N - glm::normalize(-raydirection));
		glm::vec3 recursedcolor = trace(reflectedRay, intersectionPoint, 0.005f, std::numeric_limits<float>::max(), depth - 1);
		return(Idirect + bestshape->getkm()*recursedcolor);
	}
	else {
		return(Idirect);
	}
}

void Scene::setBunnyMode(bool bunnyMode) {
	this->bunnymode = bunnyMode;
}
