// javascript-astar
// http://github.com/bgrins/javascript-astar
// Freely distributable under the MIT License.
// Implements the astar search algorithm in javascript using a binary heap.



function search(start,end,heuristic){
	var closedset = [];
	var openset = [start];
	
	var g_score = {start:0};
	var f_score = {start:heuristic(start,end)};
	
	while (openset.length>0){
		
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
