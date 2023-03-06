var i1 = 1;
var i2 = 1;
var i3 = 1;
var i4 = 1;
var i5 = 1;
var i6 = 1;
var i7 = 1;
function trigger1(){

    var mydiv = document.getElementById("hidediv1");

	if(i1%2==1){
	mydiv.style.display='none';
	}

	if(i1%2==0){
	mydiv.style.display='block';
	}

	i1++;
}

function trigger2() {

    var mydiv = document.getElementById("ul1");

    if (i2 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i2 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i2++;
}

function trigger3() {

    var mydiv = document.getElementById("ul2");

    if (i3 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i3 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i3++;
}

function trigger4() {

    var mydiv = document.getElementById("ul3");

    if (i4 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i4 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i4++;
}

function trigger5() {

    var mydiv = document.getElementById("hidediv2");

    if (i5 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i5 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i5++;
}

function trigger6() {

    var mydiv = document.getElementById("ul4");

    if (i6 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i6 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i6++;
}

function trigger7() {

    var mydiv = document.getElementById("ul5");

    if (i7 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i7 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i7++;
}

var count = 1;
function webblast2020(){
	var mydiv = document.getElementById("data_detail");

    if (count % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (count % 2 == 0) {
        mydiv.style.display = 'none';
    }

    count++;
	
} 