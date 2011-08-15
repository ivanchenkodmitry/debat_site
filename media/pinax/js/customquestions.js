//Custom qustion editor

(function($) {
    qestionnum = 0;
    answernum = 0;
    
    $( "#questioncontainer" ).sortable();
    //$( "#questioncontainer" ).disableSelection();

    
    $( "#questioncontainer" ).bind( "sortstop", updateTitles)
    
    function updateTitles(event) {
        var questions = $('#questioncontainer').sortable('toArray');
        count = questions.length;
        for (i=0;i<=count;i++) {
            $('#' + questions[i]).find('label[for="id_' + questions[i] + '_title"]').text('Питання '+ (i+1))
        }
    }
    
    $("#addquestion").click(addQestion);
//    
//    $("#submit").click({msg: 'test title'}, onSubmit);
//    
//    function onSubmit(event) {
//        $('#id_title').val(event.data.msg);
//        window.alert(event.data.msg);
//    }
    
    function addQestion(){
        var count = $("#questioncontainer").children().length;
        var num = count + 1;
        qestionnum = qestionnum + 1;
        var id = qestionnum;
        if (count < 10) { 
            $question = $('<li>');
            $question.attr('id', 'q' + id);
            $question.append('\
            <div class="ctrlHolder">\
              <label class="qtitle" for="id_q' + id +'_title">\
                Питання '+ num +'\
              </label>\
              <textarea id="id_q' + id +'_title" class="textarea" name="q' + id +'_title" cols="40" rows="10"></textarea>\
            </div>');
            $question.append('\
            <div class="ctrlHolder">\
              <label for="id_q' + id +'_type">\
                Тип відповіді\
              </label>\
              <select id="id_q' + id +'_type" name="q' + id +'_type" class="select">\
                <option selected="selected" value="1">Вільна відповіль</option>\
                <option value="2">Вибір однієї правильної</option>\
                <option value="3">Вибір кількох правильних</option>\
              </select></div>');
            $question.append('\
            <ul id="id_q' + id +'_answercontainer" class="answercontainer"></ul>');
            $question.append('\
            <div class="ctrlHolder">\
              <input id="id_q' + id +'_addanswer" type="button" value="Додати відповідь">\
              <input id="id_q' + id +'_rm" type="button" style="float:right;" value="Видалити">\
            </div>');
            //$question.append('<div class="form_block"><input id="id_q' + id +'_rm" type="button" value="Видалити"></div>');
                        
            $('#questioncontainer').append($question);
            
            $answercontainer = $('#id_q' + id +'_answercontainer');
            
            $('#id_q' + id +'_addanswer').hide();
            $answercontainer.hide();
            
            $('#id_q' + id +'_type').change({id: id}, onTypeChange);
            $('#id_q' + id +'_rm').click({id: id}, removeQestion);
            
            $answercontainer.sortable();
            $answercontainer.bind( "sortstop", {id: id}, updateAnswerTitles)
            $('#id_q' + id +'_addanswer').click({id: id}, addAnswer);
            
            $('#id_q' + id +'_addanswer').click();
            $('#id_q' + id +'_addanswer').click();
            
            var firstanswerid = $answercontainer.find('li').first().attr('id');
            $answercontainer.find('input:radio, input:checkbox').val([firstanswerid]);
        }
    }
    
    function removeQestion(event){
        $('#q' + event.data.id).remove();
        updateTitles(event);
    }
    
    function updateAnswerTitles(event) {
        var answers = $('#id_q' + event.data.id +'_answercontainer').sortable('toArray');
        count = answers.length;
        for (i=0;i<=count;i++) {
            $('#' + answers[i]).find('label[for="id_' + answers[i] + '_title"]').text('Відповідь '+ (i+1))
        }
        
    }
     
    function addAnswer(event){
        $answercontainer = $('#id_q' + event.data.id +'_answercontainer');
        var type = $('#id_q' + event.data.id +'_type').val();
        var count = $answercontainer.children().length;
        var num = count + 1;
        answernum = answernum +1;
        var id = answernum;
        if (count < 10) {        
            $ctrlholder = $('<div class="ctrlHolder">');
            $ctrlholder.append('<label for="id_a' + id +'_title"> Відповідь ' + num +'</label>');
            $ctrlholder.append('<input id="id_a' + id +'_title" class="textinput" type="text" maxlength="200" name="a' + id +'_title">');
            $ctrlholder.append('<input id="id_a' + id +'_rm" type="button" value="Видалити"><br>');
            $ctrlholder.append('<label for="id_a' + id +'_right">Правильна</label>');
            $ctrlholder.append('<input id="id_a' + id +'_rbright" class="radioboxinput" type="radio" name="q' + event.data.id +'_rbright" value="a' + id + '">');
            $ctrlholder.append('<input id="id_a' + id +'_cbright" class="checkboxinput" type="checkbox" name="a' + id +'_rbright" value="a' + id + '">');
            $answer = $('<li>');
            $answer.attr('id', 'a' + id);
            $answer.append($ctrlholder);
            $answercontainer.append($answer);
            
            switch(type)
            {
            case '2': //Вибір однієї правильної
              $answer.find('input:checkbox').hide()
              $answer.find('input:radio').show()
              break;
            case '3': //Вибір кількох правильних
              $answer.find('input:checkbox').show()
              $answer.find('input:radio').hide()
              break;
            }
        
            $('#id_a' + id +'_rm').click({id: event.data.id, aid: id}, removeAnswer);
        }
        //TODO add check handler
    }
    
    function removeAnswer(event){
        var count = $('#id_q' + event.data.id +'_answercontainer').children().length;
        if (count>2) {        
            $('#a' + event.data.aid ).remove()
        }
        updateAnswerTitles(event);
        //TODO do not remove checked answer
    }  
    
    function onTypeChange(event){
        var type = $('#id_q' + event.data.id +'_type').val();
        $answercontainer = $('#id_q' + event.data.id +'_answercontainer');
                
        switch(type)
        {
        case '1': //Вільна відповіль
          $('#id_q' + event.data.id +'_addanswer').hide();
          $answercontainer.hide();
          break;
        case '2': //Вибір однієї правильної
          $('#id_q' + event.data.id +'_addanswer').show();
          $answercontainer.show();
          $answercontainer.find('input:checkbox').hide()
          $answercontainer.find('input:radio').show()
          break;
        case '3': //Вибір кількох правильних
          $('#id_q' + event.data.id +'_addanswer').show();
          $answercontainer.show();
          $answercontainer.find('input:checkbox').show()
          $answercontainer.find('input:radio').hide()
          break;
        }
    }


})(jQuery);
