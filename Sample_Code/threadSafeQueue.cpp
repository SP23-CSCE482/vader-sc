#include <queue>
#include <mutex>
#include <condition_variable>
#include <utility>
#include <pthread.h>

class ThreadsafeQueue{
public:
	ThreadsafeQueue(size_t capacity = 500){
		maxCapacity = capacity; 
		finnishFlag = new threadObject; 
		finnishFlag->finishSignal = true;
	}
	threadObject* pop();
    bool isEmpty();
	void push(threadObject* inpElement);
	void setFullStop(bool inp);

private:
	std::queue<threadObject*> baseQueue;
	size_t maxCapacity = 500;
	bool fullStop = false;
	threadObject* finnishFlag;
	std::mutex globalMutex;
	std::condition_variable notEmptyCond;
	std::condition_variable notFullCond;
};

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

void ThreadsafeQueue::push(threadObject* inpElement){
	std::unique_lock<std::mutex> localLock(globalMutex);
	notFullCond.wait(localLock, [this] { 
		return maxCapacity > baseQueue.size(); 
	});
	baseQueue.push(inpElement);
	localLock.unlock();
	notEmptyCond.notify_one();
}

bool ThreadsafeQueue::isEmpty(){
    return baseQueue.empty();
}

void ThreadsafeQueue::setFullStop(bool inp){
    fullStop = inp;
}