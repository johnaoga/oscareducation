function make_question(parent,question_stm,q_id) {
	var d = document;
	var p = d.createElement("p");
	p.className = "lead";
	p.innerHTML = question_stm;
	var divy = d.createElement("div");
	divy.id = "StarId";
	divy.setAttribute("qid",q_id);
	divy.className = "rating-stars text-center";
	parent.append(p);
	p.append(divy);
	var ul = d.createElement("ul");
	ul.id = "stars";
	ul.innerHTML = "<b class='small'>pas du tout</b>";
	divy.append(ul);
	var array = ["Mauvais","Passable","satis","bien", "excellent"];
	for (var i=1;i<=5;i++) {
		var li = d.createElement("li");
		li.className='star small';
		li.setAttribute("data-value", i);
		li.title = array[i-1];
		ul.append(li);
		li.innerHTML = "<i class='fa fa-star fa-fw'></i>";
	}
	ul.innerHTML += "<b class='small'>excellente</b>";
};
/*
json exemple = "{ '1': 'La resource est elle complete', '2':'La resource est elle bien faite','3':'La resource est elle Nicke','4':'Dernier question pour la resource' }"
ID: resource id
*/
function makeQuestionnaire(parent,id,json) {
	json = JSON.parse(json);
	var d = document;
	var div = d.createElement("div");
	div.id = "questions";
	div.setAttribute("rid",id);
	div.style="border:1px solid grey;padding: 3px;";
	parent.append(div);
	for (var key in json) {
		make_question(div,json[key],key);
	}
	// add button
	var p = d.createElement("p");
	p.className = "small";
	p.innerHTML = "Commentaire (optionel): <br>";
	var text = d.createElement("textarea");
	text.id = "comment";
	text.maxlength = "300";
	text.rows = "7";
	p.append(text);
	div.append(p);
	var but = d.createElement("button");
	but.className = "button";
	but.id = "buttonSubmit";
	but.innerHTML = "Soumettre";
	div.append(but);

	/* IMPORTANT initFunctions() set the functions that handles all the created html!!*/
	initFunctions();
};
function send_stars(json_s) {
	/* Function to send new ratings to server and do something with return valueconsole.log(ratingValue1);
       json_s should be a json string containing 3 keys: 'id' (resource id), 'comment' and 'rated'.
       the value associated with the 'rated' key is a json with key the question id and the number
         of stars votes by to user as value.The 'comment' key is associated to a string value that
           represents the comment left by the user and id key is the resource id value
         ex. { "id": "123", "rated": { "1":"2", "2":"3"}, "comment":"I like the way comment work" }
	*/
	try {
		JSON.parse(json_s);
	} catch (e){
		console.log("invalid JSON");
		return;
	}
	$.ajax({
		url : "rate/", // the endpoint
		type : "POST", // http method
       	data : { json_str: json_s }, // data sent with the post request
       	// handle a successful response
       	success : function(json_returned) {
			// Use json to set average for each question
			console.log("success GET"+json_returned); // another sanity check
           	$(document).find("#questions").html("Votes: <br>"+json_returned);
           	$(document).parent().addClass('voted');
           	// HERE you can use returned json_returned
       	},
       	// handle a non-successful response
       	error : function(xhr,errmsg,err) {
           console.log(xhr.status + ": b" + xhr.responseText); // provide a bit more info about the error to the console
       	}
	});
};

function initFunctions() {
	var fill_board = 0;
    var update_board = setInterval(function () {
        fill_board += 1;
        $('#fillBoard').css('height', (fill_board + '%'));
        //$('#fillIcon').css('margin-top', ((100 - fill)+'%'));
        if (fill_board == 65) {
            clearInterval(update_board);
        }
    }, 10);
    var fill_hat = 0;
    var update_hat = setInterval(function () {
        fill_hat += 1;
        $('#fillHat').css('height', (fill_hat + '%'));
        //$('#fillIcon').css('margin-top', ((100 - fill)+'%'));
        if (fill_hat == 35) {
            clearInterval(update_hat);
        }
    }, 10);
    /* Default value for star rating and responses*/
    /* Handles everything when mouse over star rating */
    $('#stars li').on('mouseover', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
        // Now highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function (e) {
            if (e < onStar) {
                $(this).addClass('hover');
            }
            else {
                $(this).removeClass('hover');
            }
        });
    }).on('mouseout', function () {
        $(this).parent().children('li.star').each(function (e) {
            $(this).removeClass('hover');
        });
    });
    $("#buttonSubmit").on('click', function () {
    	var s = $(".rating-stars");
    	var json = new Object();
        var r = new Object();
        var id = $("#questions").attr('rid');
        var count = 0;
        for (var i=0;i<s.length;i++) {
			if (s[i].getAttribute("stars") != undefined) {
				count+=1;
			}
			r[s[i].getAttribute("qid")] = s[i].getAttribute("stars");
		}
		if (count != s.length) {
        	alert('Veiller répondre à toutes les questions')
		} else {
        	var comment = $("#comment").val();
        	json["id"] = id;
        	json["comment"] = comment;
        	json["rated"] = r;
        	$("#questions").addClass("voted");
        	//send_stars(JSON.stringify(json));
			console.log(JSON.stringify(json));
		}
    });
    /* Handles everything when we click on the stars */
    $('#stars li').on('click', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');
        var parent = $(this).parent().parent();
        parent.attr("stars", onStar);
        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }
        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
    });
    $('[data-popup-open]').on('click', function (e) {
        var targeted_popup_class = jQuery(this).attr('data-popup-open');
        $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
        $("#chartContainer").CanvasJSChart({ //Pass chart options
            animationEnabled: true,
            theme: "light1",
            axisY: {
                title: "Nombre d'étoiles"
            },
            data: [
                {
                    type: "column", //change it to column, spline, line, pie, etc
                    dataPoints: [
                        {y: 3.5, label: "exactitude"},
                        {y: 2.7, label: "complétude"},
                        {y: 4.2, label: "compréhensibilité"},
                        {y: 1.9, label: "pertinance"}
                    ]
                }
            ]
        });
        chart.render();
        e.preventDefault();
    });
    $('[data-popup-open]').on('click', function (e) {
        var targeted_popup_class = jQuery(this).attr('data-popup-open');
        $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
        $("#chartContainer").CanvasJSChart({ //Pass chart options
            animationEnabled: true,
            theme: "light1",
            axisY: {
                title: "Nombre d'étoiles"
            },
            data: [
                {
                    type: "column", //change it to column, spline, line, pie, etc
                    dataPoints: [
                        {y: 3.5, label: "exactitude"},
                        {y: 2.7, label: "complétude"},
                        {y: 4.2, label: "compréhensibilité"},
                        {y: 1.9, label: "pertinance"}
                    ]
                }
            ]
        });
        chart.render();
        e.preventDefault();
    });
};
