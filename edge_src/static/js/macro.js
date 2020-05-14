//function set_pop_btn(btn,bac){
//    btn.click(function(){
//    bac.show();
//    });
//}

function pop_up_ready(){


$("#open_btn").click(function(){
$("#background").show();
});

$("#close-button").click(function(){
$("#background").hide();
});

$("button.train_btn").each(
function(){
$("this").click(
function(){
$("#background").show();
});
}
);
}