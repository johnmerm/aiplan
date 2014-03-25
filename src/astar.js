// javascript-astar
// http://github.com/bgrins/javascript-astar
// Freely distributable under the MIT License.
// Implements the astar search algorithm in javascript using a binary heap.


var BinaryHeap = require('./binaryheap.js').BinaryHeap;

function reconstruct_path(node,came_from){
	var p=[];
	while (true){
		p.unshift(node)
		if (node in came_from){
			node = came_from[node];
		}else{
			return p;
		}
	}
}
function search(start,end,heuristic,neighbors){
	
	var dist = function(parent,node){
		return 1;
	}
	var closedset = {};
	var openset = {start:true};
	
	var g_score = {start:0};
	var f_score = {start:heuristic(start,end)};
	
	var priorityQueue = new BinaryHeap(function score(node) {
		return f_score[node];
	});
	priorityQueue.push(start);
	
	
	var came_from={}
	
	while (openset.length>0){
		current = priorityQueue.pop();
		if (current == end){
			return reconstruct_path(end, came_from);
		}
		
		delete openset[current];
		closedset[current] = true;
		nn = neighbors(current);
		for (n in nn){
			if (n in closedset){
				continue;
			}
			var tentative_g = g_score[current]+dist(current, n);
			if (!(n in openset) || tentative_g<g_score[n]){
				came_from[n] = current;
				g_score[n] = tentative_g;
				f_score[n] = g_score[n]+heuristic(n)
				if (!(n in openset)){
					openset[n] = true;
				}
			}
		}
		
	}
	
	
}


function testAstar(){
	var EightPuzzle = require('./eightpuzzle.js');
	var start = new EightPuzzle("164870325");
	var end   = new EightPuzzle("012345678");
	var path= search(start, end, function(current){
		return current.manhattan();
	});
	
	console.log(path.length);
}

testAstar();
