// For an array of numbers, return the maximal substring in O(n) time

if (typeof(alert) == 'undefined') {
	global.alert = mesg => console.log(mesg);
}

function getMaxSubSum(arr) {
	let maxsum=Number.NEGATIVE_INFINITY, bestLeft=0, bestRight=0;

	// Find the maximal subarray sum from index 0 to n, where n<arr.length
	let currLeft=0;
	for (let i=0, currsum=0; i<arr.length; i++) {
		if (currsum < 0) {
			currsum=0;
			currLeft=i;
		}

		currsum+=arr[i];
		if (currsum > maxsum) {
			maxsum=currsum;
			bestRight=i+1;
			bestLeft=currLeft;
		}
	}

	if (maxsum <= 0) {
		maxsum=0;
		bestLeft=0;
		bestRight=0;
	}
  
	alert(`For this array:${arr}\nMaxSum of ${maxsum} acheived with subarray indexes ${bestLeft} to ${bestRight}\nYielding this subarray: ${arr.slice(bestLeft, bestRight)}`);
	return maxsum;
}

getMaxSubSum([-1, 2, 3, -9]);
getMaxSubSum([2, -1, 2, 3, -9]);
getMaxSubSum([-1, 2, 3, -9, 11]);
getMaxSubSum([-2, -1, 1, 2]);
getMaxSubSum([100, -9, 2, -3, 5]);
getMaxSubSum([1, 2, 3]);
getMaxSubSum([-1, -2]);
getMaxSubSum([1, 2, -1000, 5]);