var i1 = 1;
var i2 = 1;
var i3 = 1;

function trigger1(){

    var mydiv = document.getElementById("ul1");

	if(i1%2==1){
	mydiv.style.display='none';
	}

	if(i1%2==0){
	mydiv.style.display='block';
	}

	i1++;
}

function trigger2() {

    var mydiv = document.getElementById("ul2");

    if (i2 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i2 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i2++;
}

function trigger3() {

    var mydiv = document.getElementById("ul3");

    if (i3 % 2 == 1) {
        mydiv.style.display = 'block';
    }

    if (i3 % 2 == 0) {
        mydiv.style.display = 'none';
    }

    i3++;
}

