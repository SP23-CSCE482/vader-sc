#include "BVH.h"
#include <iostream>
#include <algorithm>

BVH::BVH(){
	this->maxPoint = glm::vec3(0.0f, 0.0f, 0.0f);
	this->minPoint = glm::vec3(0.0f, 0.0f, 0.0f);
}

BVH::~BVH()
{
	for (size_t i = 0; i < this->children.size(); i++) {
		delete children.at(i);
	}
}

Intersection BVH::intersect(glm::vec3 raydirection, glm::vec3 rayorigin) {
	float ix1 = (minPoint[0] - rayorigin[0]) / raydirection[0];
	float ix2 = (maxPoint[0] - rayorigin[0]) / raydirection[0];

	float tmin = glm::min(ix1, ix2);
	float tmax = glm::max(ix1, ix2);

	float iy1 = (minPoint[1] - rayorigin[1]) / raydirection[1];
	float iy2 = (maxPoint[1] - rayorigin[1]) / raydirection[1];

	float tymin = glm::min(iy1, iy2);
	float tymax = glm::max(iy1, iy2);

	if ((tmin > tymax) || (tymin > tmax)) {
		Intersection output = Intersection{ -1.0f, nullptr, false };
		return output;
	}
	tmin = glm::max(tmin, tymin);
	tmax = glm::min(tmax, tymax);

	float iz1 = (minPoint[2] - rayorigin[2]) / raydirection[2];
	float iz2 = (maxPoint[2] - rayorigin[2]) / raydirection[2];

	float tzmin = glm::min(iz1, iz2);
	float tzmax = glm::max(iz1, iz2);

	if ((tmin > tzmax) || (tzmin > tmax)) {
		Intersection output = Intersection{ -1.0f, nullptr, false };
		return output;
	}
	tmin = glm::max(tmin, tzmin);
	tmax = glm::min(tmax, tzmax);
	//std::cout << "made it past 1st round BVH intersection" << tmin << " " << tmax << std::endl;
	if (tmin >= 0.0f || tmax >= 0.0f) {
		float mint = std::numeric_limits<float>::max();
		Shape* bestshape = nullptr;
		bool didhit = false;
		float t0 = 0.005f;
		glm::vec3 rayoriginp = rayorigin + (raydirection)*t0; //shoot ray from a point t0*raydirection away from rayorigin

		//find closest intersection
		for (Shape* shape : this->children) {
			Intersection intersection = shape->intersect(raydirection, rayoriginp);
			float intersectiontime = intersection.t + t0;//adjust intersectiontime by t0 since rayorigin was adjusted by t0
			if (intersectiontime < mint && intersectiontime >= t0 && intersectiontime < std::numeric_limits<float>::max()) {
				bestshape = (Shape*)intersection.intersectedShape;
				mint = intersectiontime;
				didhit = true;
			}
		}
		//std::cout << "made it past 2nd round BVH intersection" << std::endl;
		Intersection output = { mint, bestshape, didhit };
		return(output);

		//PSEUDOCODE
		//if leaf node, return Intersection struct
		//else, call intersect on child because it's not a triangle, it's another BVH.
	}
	else {
		Intersection output = { tmax, nullptr, false };
		return(output);
	}
}
	
void BVH::pushShape(Shape* shape)
{
	this->updateBounds(shape);
	this->children.push_back(shape);
}

void BVH::buildBVH()
{	
	//check if the BVH should be split in the first place
	if (this->children.size() > 3) {
		//sort according to depth (1 == x, 2 == y, 3 == z, 4 == x, ...)
		int depth = this->depth;//for passing to capture clause of lambda function
		std::sort(children.begin(),children.end(),[depth](Shape* a, Shape* b) {
			return (a->getAveragePosition()[depth % 3] < b->getAveragePosition()[depth % 3]);
			}
		);

		//see if the sorting worked
		/*for (int i = 0; i < children.size(); i++) {
			std::cout << "trianle no " << i << " after sorting has x coordinate " << children.at(i)->getAveragePosition()[0] << std::endl;
		}*/

		//split sorted triangles in two
		int middle = children.size() / 2;
		//create two more BVH objects and set as children
		Shape* BVH1 = new BVH();
		Shape* BVH2 = new BVH();

		//these BVHs will be 1 deeper than the current BVH
		BVH1->depth = this->depth + 1;
		BVH2->depth = this->depth + 1;

		//assign children, in the process creating the correctly sized bounding boxes
		for (int i = 0; i < middle; i++) {
			BVH1->pushShape(children.at(i));
		}
		for (int i = middle; i < children.size(); i++) {
			BVH2->pushShape(children.at(i));
		}		
		//call buildBVH on these children
		BVH1->buildBVH();
		BVH2->buildBVH();

		//reset children list and push back the two BVH objects as new chidren
		this->children.clear();
		this->children.push_back(BVH1);
		this->children.push_back(BVH2);
	}
	else {
		//do nothing
	}
}

glm::vec3 BVH::getAveragePosition()
{
	return((minPoint + maxPoint) * 0.5f); //probably won't use this function in this context, but it just represents the center of the box
}

Extent BVH::getMaxExtent()
{
	return Extent { minPoint,maxPoint };
}

void BVH::updateBounds(Shape* newShape)
{
	if (this->children.size() == 0) {
		Extent shapeExtent = newShape->getMaxExtent();
		this->minPoint = shapeExtent.minPoint;
		this->maxPoint = shapeExtent.maxPoint;
	}
	else {
		Extent shapeExtent = newShape->getMaxExtent();

		glm::vec3 newmin = glm::vec3{ glm::min(shapeExtent.minPoint[0], minPoint[0]),
		glm::min(shapeExtent.minPoint[1], minPoint[1]) ,
		glm::min(shapeExtent.minPoint[2], minPoint[2]) };

		glm::vec3 newmax = glm::vec3{ glm::max(shapeExtent.maxPoint[0], maxPoint[0]),
		glm::max(shapeExtent.maxPoint[1], maxPoint[1]) ,
		glm::max(shapeExtent.maxPoint[2], maxPoint[2]) };

		this->minPoint = newmin;
		this->maxPoint = newmax;
	}
	
}

//never use any of these
glm::vec3 BVH::getNormal(glm::vec3 intersectionPoint) {
	return(glm::vec3(1.0f, 0.0f, 0.0f));
}

glm::vec3 BVH::getka() {
	return(glm::vec3(1.0f, 0.0f, 0.0f));
}

glm::vec3 BVH::getkd() {
	return(glm::vec3(1.0f, 0.0f, 0.0f));
}

glm::vec3 BVH::getks() {
	return(glm::vec3(1.0f, 0.0f, 0.0f));
}

glm::vec3 BVH::getkm() {
	return(glm::vec3(1.0f, 0.0f, 0.0f));
}

float BVH::getn() {
	return(1.0f);
}
