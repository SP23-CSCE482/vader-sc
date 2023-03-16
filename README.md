# Experimental GPT-J Vader-SC
This is the repository for VADER-SC - A project to increase source code readability. <br />
Uses GPT-J multishot to generate comments. <br />
Requires 48GB of Ram to load the complete model and 16GB VRAM to run infererence. <br />
Needs 30GB of available space. <br />
Requires an NVIDIA GPU.<br />

## Some Samples
```C++
// Generated: 
/*******************************************************************************
* 
*   This function takes a picture of the scene.
*   It uses the raytracing algorithm to calculate the color of each pixel.
*   It then renders the image to the screen.
*
* Inputs:
*   scene - the scene to be rendered
*
* Outputs:
*   renderedImage - the rendered image
*******************************************************************************/

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
```

```C++
// Generated: 
/*******************************************************************************
* 
*   This function checks if the queue is full.
*   If it is, then it sets the finnishFlag to true.
*
* Inputs:
*   finnishFlag - a flag to indicate if the queue is full
*******************************************************************************/

threadObject* ThreadsafeQueue::pop(){
	std::unique_lock<std::mutex> localLock(globalMutex);
	notEmptyCond.wait(localLock, [this] { 
		if(fullStop && baseQueue.empty()){
			return true;
		} 
		return !baseQueue.empty(); 
	});

	if(fullStop && baseQueue.empty()){
		return finnishFlag;
	}
	threadObject* inpElement = baseQueue.front();
	baseQueue.pop();
	localLock.unlock();
	notFullCond.notify_one();
	return inpElement;
}
```


## Usage
To parse directory run ```python3 vader.py /path/to/directory```

## Local Setup 
* If you don't have ctags installed (which is a system requirement to run the philips parser), run ```sudo apt-get install exuberant-ctags```
* create a virtual environment, and install the requirements. 
  * Run ```python3 -m venv SC_Venv && source SC_Venv/bin/activate && pip install -r requirements.txt -vvv```     
