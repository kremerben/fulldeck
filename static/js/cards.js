
function toggleRotate() {
    $("#joker").toggleClass("rotate");
    $("#black_joker").toggleClass("neg_rotate");
}

setInterval(toggleRotate, 500);

