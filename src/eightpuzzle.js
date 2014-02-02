function EightPuzzle(string){
	
	this.cols = Math.sqrt(string.length);
	this.rows = this.cols;
	
	this.string = string;
}

EightPuzzle.prototype = {
	neighbors:function(){
		var string = this.string;
		
		var swap = function(i,j){
			var array = string.split('');
			var  sw = array[i];
			array[i] = array[j];
			array[j] = sw;
			return array.join('');
		};
		
		
		
		var cols = this.cols;
		var rows = this.rows;
		
		
		var pos = string.indexOf('0');
		var col = Math.floor(pos/cols);
		var row = pos % rows;
		var n = [];
		
		var newpos = null;
		var newString = null;
		if (col>0){
			newpos = (col-1)*rows+row;
			var ep = new EightPuzzle(swap(pos,newpos));
			ep.cost = 1;
			n.push(ep);
		}
		
		if (col<cols-1){
			newpos = (col+1)*rows+row;
			var ep = new EightPuzzle(swap(pos,newpos));
			ep.cost = 1;
			n.push(ep);
		}
		
		
		if (row>0){
			newpos = col*rows+(row-1);
			var ep = new EightPuzzle(swap(pos,newpos));
			ep.cost = 1;
			n.push(ep);
		}
		
		if (row<rows-1){
			newpos = col*rows+(row+1);
			var ep = new EightPuzzle(swap(pos,newpos));
			ep.cost = 1;
			n.push(ep);
		}
		
		return n;
	},
	
	manhattan:function (){
		var string = this.string;
		var distance = 0;
		
		var cols = this.cols;
		var rows = this.rows;
		
		
		var pos = string.indexOf('0');
		
		for (pos=0;pos<string.length;pos++){
			var col = Math.floor(pos/cols);
			var row = pos % rows;
			
			var c_pos = parseInt(string[pos],10);
			var c_col = Math.floor(c_pos/cols);
			var c_row = c_pos % rows;
			
			distance += (Math.abs(c_pos-pos)+Math.abs(c_row-row));
			
		}
		return distance;
	},
	toString:function(){
		var retString = "";
		
		for (var i=0;i<this.cols;i++){
			for (var j=0;j<this.rows;j++){
				var p = i*this.rows+j;
				var c = this.string[p];
				if (c !== '0'){
					retString += c;
				}else{
					retString += ' ';
				}
			}
			retString+= '\n';
		}
		return retString;
	}
};

module.exports = EightPuzzle;

function testEightPuzzle(){
	var eightPuzzle = new EightPuzzle("164870325");
	console.log(eightPuzzle.toString());
	console.log(eightPuzzle.manhattan());
	var neighbors = eightPuzzle.neighbors();
	
	for ( var i in neighbors) {
		console.log(neighbors[i].toString());
		console.log(neighbors[i].manhattan());
		
	}
}


