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
*   This function pops the first element from the queue.
*
* Inputs:
*   inpElement - the element to pop from the queue
*
* Outputs:
*   none
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
* To parse directory run ```python3 vader.py /path/to/directory```

* To use GUI cd into vader-sc/ and run ```./vader-gui.sh``` or run ```source SC_Venv/bin/activate && python3 vader-gui.py```

* If using WSL, performance will be very slow to analyze mounted folders (/mnt/c/)
* Consider moving folders into WSL, then generating comments within WSL

## Installation Script
* Make sure you are not in any existing python environments and that you atleast have python 3.6 installed
* To install using the script you must be root and you must run ```chmod +x install.sh && sudo ./install.sh``` inside the folder.
* You must download the model when prompted so the program runs properly (~800+ MB).
* You can add alias to the program by running ```alias vader-sc='$PWD/SC_Venv/bin/python3 $PWD/vader.py'``` so it can be used anywhere
* To run the program without an alias you can do ```source SC_Venv/bin/activate``` and then use ```python3 vader.py```.
* If you get the error ```Error no file named ...```. Please rerun the installation script and download the model when prompted or get it [here](https://storage.googleapis.com/model_bucket_for_capstone_tamu/pytorch_model.bin) and place it in the directory where vader.py is located.
* if you have any issues with the installtion script please do a manual installation.

## Local Setup 
* If you don't have ctags installed (which is a system requirement to run the philips parser), run ```sudo apt-get install exuberant-ctags```

* To run the gui, you need to install python3-tk as well
* Run ```sudo apt-get install python3-tk```

* cd into the directory vader-sc 

* create a virtual environment, and install the requirements. 
  * Run ```python3 -m venv SC_Venv && source SC_Venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt -vvv```     
