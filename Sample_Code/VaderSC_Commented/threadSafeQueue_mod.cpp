#include <queue>
#include <mutex>
#include <condition_variable>
#include <utility>
#include <pthread.h>

class ThreadsafeQueue{
public:
// Generated: Queue for thread safe processing.
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

// Generated: pop an element from the queue or do full stop if there are no more elements to pop
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

// Generated: Push an element onto the queue.
void ThreadsafeQueue::push(threadObject* inpElement){
	std::unique_lock<std::mutex> localLock(globalMutex);
	notFullCond.wait(localLock, [this] { 
		return maxCapacity > baseQueue.size(); 
	});
	baseQueue.push(inpElement);
	localLock.unlock();
	notEmptyCond.notify_one();
}

// Generated: Returns true if the queue is empty.
bool ThreadsafeQueue::isEmpty(){
    return baseQueue.empty();
}

// Generated: set full stop state
void ThreadsafeQueue::setFullStop(bool inp){
    fullStop = inp;
}