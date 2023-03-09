#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <vector>
#include <chrono>
#include <iostream>
#include "Camera.h"
#include "Scene.h"
#include "Triangle.h"
#include "Sphere.h"
#include "BVH.h"
#define TINYOBJLOADER_IMPLEMENTATION
#include "tiny_obj_loader.h"

std::vector<float> posBuff;
std::vector<float> norBuff;
std::vector<float> texBuff;

#define WINDOW_HEIGHT 800
#define WINDOW_WIDTH 1200

float frameBuffer[WINDOW_HEIGHT][WINDOW_WIDTH][3];
GLFWwindow *window;

std::vector<Shape*> shapes;
std::vector<Light*> lights;

// Generated: Loads a model from file.
void LoadModel(char* name)
{
	// Taken from Shinjiro Sueda with slight modification
	std::string meshName(name);
	tinyobj::attrib_t attrib;
	std::vector<tinyobj::shape_t> shapes;
	std::vector<tinyobj::material_t> materials;
	std::string errStr;
	bool rc = tinyobj::LoadObj(&attrib, &shapes, &materials, &errStr, meshName.c_str());
	if (!rc) {
		std::cerr << errStr << std::endl;
	}
	else {
		// Some OBJ files have different indices for vertex positions, normals,
		// and texture coordinates. For example, a cube corner vertex may have
		// three different normals. Here, we are going to duplicate all such
		// vertices.
		// Loop over shapes
		for (size_t s = 0; s < shapes.size(); s++) {
			// Loop over faces (polygons)
			size_t index_offset = 0;
			for (size_t f = 0; f < shapes[s].mesh.num_face_vertices.size(); f++) {
				size_t fv = shapes[s].mesh.num_face_vertices[f];
				// Loop over vertices in the face.
				for (size_t v = 0; v < fv; v++) {
					// access to vertex
					tinyobj::index_t idx = shapes[s].mesh.indices[index_offset + v];
					posBuff.push_back(attrib.vertices[3 * idx.vertex_index + 0]);
					posBuff.push_back(attrib.vertices[3 * idx.vertex_index + 1]);
					posBuff.push_back(attrib.vertices[3 * idx.vertex_index + 2]);
					if (!attrib.normals.empty()) {
						norBuff.push_back(attrib.normals[3 * idx.normal_index + 0]);
						norBuff.push_back(attrib.normals[3 * idx.normal_index + 1]);
						norBuff.push_back(attrib.normals[3 * idx.normal_index + 2]);
					}
					if (!attrib.texcoords.empty()) {
						texBuff.push_back(attrib.texcoords[2 * idx.texcoord_index + 0]);
						texBuff.push_back(attrib.texcoords[2 * idx.texcoord_index + 1]);
					}
				}
				index_offset += fv;
				// per-face material (IGNORE)
				shapes[s].mesh.material_ids[f];
			}
		}
	}
}

// Generated: Clear the frame buffer
void ClearFrameBuffer()
{
	memset(&frameBuffer, 0, WINDOW_HEIGHT * WINDOW_WIDTH * 3 * sizeof(float));
}

// Generated: Display function, called when window is opened.
void Display()
{	
	glDrawPixels(WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGB, GL_FLOAT, frameBuffer);
}

// Generated: Initializes OpenGL, and starts the window.
void Init()
{
	glfwInit();
	glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);
	window = glfwCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, "Assignment5 - Anthony Pierson", NULL, NULL);
	glfwMakeContextCurrent(window);
	glewExperimental = GL_TRUE;
	glewInit();

	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	ClearFrameBuffer();

	bool bunnymode = false;
	while (true) {
		std::cout << "choose your mode: " << std::endl;
		std::cout << "b: bunny (task 3)" << std::endl;
		std::cout << "s: standard scene (task 2)" << std::endl;
		char selection;
		std::cin >> selection;
		if (selection == 'b') {
			bunnymode = true;
			break;
		}
		if (selection == 's') {
			bunnymode = false;
			break;
		}
	}
	



	//LoadModel("../../obj/naboo.obj");//change this path if it is not pointing to the right location for you
	LoadModel("../../obj/bunny.obj");//change this path if it is not pointing to the right location for you
	Scene scene = Scene(bunnymode);

	if (bunnymode) {
		Shape* bvh = new BVH();

		for (size_t i = 0; i < posBuff.size(); i += 9) {
			Shape* tri = new Triangle(
				glm::vec3(norBuff[i + 0], norBuff[i + 1], norBuff[i + 2]),
				glm::vec3(norBuff[i + 3], norBuff[i + 4], norBuff[i + 5]),
				glm::vec3(norBuff[i + 6], norBuff[i + 7], norBuff[i + 8]),
				glm::vec3(posBuff[i + 0], posBuff[i + 1], posBuff[i + 2]),
				glm::vec3(posBuff[i + 3], posBuff[i + 4], posBuff[i + 5]),
				glm::vec3(posBuff[i + 6], posBuff[i + 7], posBuff[i + 8]),
				glm::vec3(0.1f, 0.1f, 0.1f),
				glm::vec3(0.0f, 0.0f, 1.0f),
				glm::vec3(1.0f, 1.0f, 0.5f),
				glm::vec3(0.0f, 0.0f, 0.0f),
				100.0f
			);
			bvh->pushShape(tri);
		}
		bvh->buildBVH();//build the BVH after pushing all tris
		scene.pushShape(bvh);
	}

	
	

	Camera camera = Camera(WINDOW_WIDTH,
							WINDOW_HEIGHT,
							glm::vec3(0.0f, 0.0f, 7.0f),
							glm::vec3(0.0f, 0.0f, 0.0f), 
							glm::vec3(0.0f, 1.0f, 0.0f), 
							45.0f, 
							1.0f );
	
	auto start = std::chrono::high_resolution_clock::now();
	camera.TakePicture(&scene);
	auto stop = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);
	std::cout << "Time passed (ms): " << duration.count() << std::endl;
	
	float *renderedImage = camera.GetRenderedImage();
	memcpy(frameBuffer, renderedImage, sizeof(float) * WINDOW_HEIGHT * WINDOW_WIDTH * 3);
}


// Generated: Main entry point for the program.
int main()
{	
	Init();
	while ( glfwWindowShouldClose(window) == 0) 
	{
		glClear(GL_COLOR_BUFFER_BIT);
		Display();
		glFlush();
		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	glfwTerminate();
	return 0;
}