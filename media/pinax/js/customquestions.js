//Custom qustion editor

(function( $ ){

  $.fn.testeditor = function() {
        
    this.find(':submit').remove();
    
    this.after('\
            <h2>Додаткові питання</h2>\
            <form class="uniForm">\
              <fieldset class="inlineLabels">\
                <ul id="itemcontainer">\
                </ul>\
                <div class="form_block" style="padding: 7px;">\
                    <a id="additem">Додати питання</a>\
                </div>\
                <div class="form_block">\
                    <input id="psevdosubmit" type="button" value="Надіслати">\
                </div>\
              </fieldset>\
            </form>');
    
    var itemnum = 0,
        optionnum = 0;
        
    $("#itemcontainer").sortable();
    //$( "#itemcontainer" ).disableSelection();
            
    $("#additem").click(onAddItem);
    
    $("#itemcontainer" ).bind( "sortstop", onUpdateTitles)
    
    this.submit(onSubmit); 
               
    $('#psevdosubmit').click(function() {
    $("#edit-profile").submit();
    });
    
    var data = $('#id_questions').val();
    
    if (data != '')  {       
        var data = $.secureEvalJSON(data);
        for (var i=0;i<data.length;i++) {
            addItem(data[i]);
        }
    }
        
    function onAddItem(event){
        addItem();
    }
    
    function addItem(data){
        var count = $("#itemcontainer").children().length;
        var num = count + 1;
        itemnum = itemnum + 1;
        var id = itemnum;
        if (count < 10) { 
            $item = $('\
                <li id="i'+id +'">\
                  <div class="ctrlHolder">\
                    <label class="itemtitle" for="id_i' + id +'_title">\
                      Питання '+ num +'\
                    </label>\
                    <textarea id="id_i' + id +'_title" class="textarea" cols="40" rows="10"></textarea>\
                    <a id="id_i' + id +'_rm" style="float:right;">X</a>\
                  </div>\
                  <div class="ctrlHolder">\
                    <label for="id_i' + id +'_type">Тип відповіді</label>\
                    <select id="id_i' + id +'_type" class="select">\
                      <option selected="selected" value="1">Вільна відповіль</option>\
                      <option value="2">Вибір однієї правильної</option>\
                      <option value="3">Вибір кількох правильних</option>\
                    </select>\
                  </div>\
                  <ul id="id_i' + id +'_optioncontainer" class="optioncontainer"></ul>\
                  <div id="div_id_i' + id +'_addoption" class="ctrlHolder">\
                    <a id="id_i' + id +'_addoption">Додати відповідь</a>\
                  </div>\
                </li>');
                
            //TODO type names
                        
            $('#itemcontainer').append($item);
            
            $optioncontainer = $('#id_i' + id +'_optioncontainer');
            
            $('#div_id_i' + id +'_addoption').hide();
            $optioncontainer.hide();
            
            $('#id_i' + id +'_type').change({id: id}, onTypeChange);
            $('#id_i' + id +'_rm').click({id: id}, removeItem);
            
            $optioncontainer.sortable();
            $optioncontainer.bind( "sortstop", {itemid: id}, updateOptionTitles)
            $('#id_i' + id +'_addoption').click({id: id}, onAddOption);
            
            if (data != undefined) {
                $('#id_i' + id +'_title').val(data.title)
                $('#id_i' + id +'_type').val(data.type)
                $('#id_i' + id +'_type').change()
                console.log(data.type);
                if (data.type != '1') {
                    console.log(data.options);
                    for (var j=0;j<data.options.length;j++) {
                        addOption(id,data.options[j]);
                    }
                    return true;
                }
            }
            
            addOption(id, {right: true});
            addOption(id);
            
        }
    }
    
    function removeItem(event){
        $('#i' + event.data.id).remove();
        updateTitles();
    }
    
    function onUpdateTitles(event) {
        updateTitles();
    }
    
    function updateTitles() {
        $('#itemcontainer > li').each(function(i) {
            //TODO
            $(this).find('label.itemtitle').text('Питання '+ (i+1))
        });
    }
    
    function onAddOption(event){        
        addOption(event.data.id);
    }
    
    function addOption(itemid, data){
        $optioncontainer = $('#id_i' + itemid +'_optioncontainer');
        var type = $('#id_i' + itemid +'_type').val();
        var count = $optioncontainer.children().length;
        var num = count + 1;
        optionnum = optionnum +1;
        var id = optionnum;
        if (count < 10) {        
            $option = $('\
                <li id="o'+ id +'">\
                  <div class="ctrlHolder">\
                    <label for="id_o' + id +'_title"> Відповідь ' + num +'</label>\
                    <input id="id_o' + id +'_title" class="textinput" type="text" maxlength="200">\
                    <a id="id_o' + id +'_rm">X</a><br>\
                    <label for="id_o' + id +'_right">Правильна</label>\
                    <input id="id_o' + id +'_rbright" class="radioboxinput" type="radio"\
                           name="i' + itemid +'_rbright" value="o' + id + '">\
                    <input id="id_o' + id +'_cbright" class="checkboxinput" type="checkbox"\
                           name="o' + id +'_rbright" value="o' + id + '">\
                  </div>\
                </li>');

            $optioncontainer.append($option);
            
            if (data != undefined) {

            if (data.title != undefined) {
                $('#id_o' + id +'_title').val(data.title);
            }
            
            //XXX 1 first radio checked only
            if (data.right != undefined) {
                $('#id_o' + id +'_cbright').attr('checked', data.right);
                $('#id_o' + id +'_rbright').attr('checked', data.right);
            }
            
            }
            
            switch(type)
            {
            case '2': //Вибір однієї правильної
              $option.find('input:checkbox').hide()
              $option.find('input:radio').show()
              break;
            case '3': //Вибір кількох правильних
              $option.find('input:checkbox').show()
              $option.find('input:radio').hide()
              break;
            }
        
            $('#id_o' + id +'_rm').click({itemid: itemid, optionid: id}, removeOption);
        }
        //TODO 2 add check handler (see 4)
    }
    
    function removeOption(event){
        var count = $('#id_i' + event.data.itemid +'_optioncontainer').children().length;
        if (count>2) {        
            $('#o' + event.data.optionid ).remove()
        }
        updateOptionTitles(event);
        //TODO 3 do not remove checked option (see 4)
    }   
    
    function updateOptionTitles(event) {
        $('#id_i' + event.data.itemid +'_optioncontainer > li').each(function(i) {
            $(this).find('label[for$="_title"]').text('Відповідь '+ (i+1));
        });
    }
    
    function onTypeChange(event){
        var type = $('#id_i' + event.data.id +'_type').val();
        $optioncontainer = $('#id_i' + event.data.id +'_optioncontainer');
                
        switch(type)
        {
        case '1': //Вільна відповіль
          $('#div_id_i' + event.data.id +'_addoption').hide();
          $optioncontainer.hide();
          break;
        case '2': //Вибір однієї правильної
          $('#div_id_i' + event.data.id +'_addoption').show();
          $optioncontainer.show();
          $optioncontainer.find('input:checkbox').hide()
          $optioncontainer.find('input:radio').show()
          break;
        case '3': //Вибір кількох правильних
          $('#div_id_i' + event.data.id +'_addoption').show();
          $optioncontainer.show();
          $optioncontainer.find('input:checkbox').show()
          $optioncontainer.find('input:radio').hide()
          break;
        }
    }
    
    function getData(){
        var items = $('#itemcontainer').sortable('toArray');
        
        var types = {
            '2':'radio',
            '3':'checkbox'        
        }
        
        var data = new Array();    
        
        $('#itemcontainer > li').each(function(i) {
            var item = new Object();
            item.title = $(this).find('textarea').val();
            item.type = $(this).find('select').val();
            if (item.type != '1') {
                item.options = new Array();
                $(this).find('li').each(function(j) {
                    var option = new Object();
                    option.title = $(this).find('input:text').val();
                    if ($(this).find('input:'+ types[item.type]).attr('checked')) {
                        option.right = true;
                    }
                    item.options.push(option);
                });
            }            
            data.push(item);
        });
        return data;
    }
    
    function onSubmit(event) {
        $('#id_questions').val($.toJSON(getData()));
        return true;
        //TODO 4 add some validation
    }

  };
})( jQuery );
