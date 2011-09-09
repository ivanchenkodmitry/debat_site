//Custom qustion editor

(function( $ ){

  $.fn.testeditor = function() {
    
    submit = this.find(':submit').val()
    
    this.find(':submit').remove();
    
    this.after('\
            <h2>Додаткові питання</h2>\
            <form class="uniForm">\
              <fieldset class="inlineLabels">\
                <ul id="itemcontainer">\
                </ul>\
                <div class="form_block" style="padding: 7px;">\
                    <a id="additem" href="javascript: void(0)">Додати питання</a>\
                </div>\
                <div class="form_block">\
                    <input id="psevdosubmit" type="button" value="'+ submit +'">\
                </div>\
              </fieldset>\
            </form>');
    
    var itemnum = 0,
        optionnum = 0,
        maxitem = 10,
        maxoption = 10;
        
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
        if (count < maxitem) { 
            $item = $('\
                <li id="i'+id +'">\
                  <div class="ctrlHolder">\
                    <label class="itemtitle" for="id_i' + id +'_title">\
                      Питання '+ num +'\
                    </label>\
                    <textarea id="id_i' + id +'_title" class="textarea" cols="40" rows="10"></textarea>\
                    <a id="id_i' + id +'_rm" class="rmlink" href="javascript: void(0)">X</a>\
                  </div>\
                  <div class="ctrlHolder">\
                    <label for="id_i' + id +'_type">Тип відповіді</label>\
                    <select id="id_i' + id +'_type" class="select">\
                      <option selected="selected" value="free">Вільна відповіль</option>\
                      <option value="one">Вибір однієї відповіді</option>\
                      <option value="multi">Вибір кількох відповідей</option>\
                    </select>\
                  </div>\
                  <ul id="id_i' + id +'_optioncontainer" class="optioncontainer"></ul>\
                  <div id="div_id_i' + id +'_addoption" class="ctrlHolder">\
                    <a id="id_i' + id +'_addoption" href="javascript: void(0)">Додати відповідь</a>\
                  </div>\
                </li>');

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
                if (data.type != 'free') {
                    console.log(data.options);
                    for (var j=0;j<data.options.length;j++) {
                        addOption(id,data.options[j]);
                    }
                    return true;
                }
            }
            
            addOption(id);
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
    
    function addOption(itemid, title){
        $optioncontainer = $('#id_i' + itemid +'_optioncontainer');
        var count = $optioncontainer.children().length;
        var num = count + 1;
        optionnum = optionnum +1;
        var id = optionnum;
        if (count < maxoption) {        
            $option = $('\
                <li id="o'+ id +'">\
                  <div class="ctrlHolder">\
                    <label for="id_o' + id +'_title"> Відповідь ' + num +'</label>\
                    <input id="id_o' + id +'_title" class="textinput" type="text" maxlength="200">\
                    <a id="id_o' + id +'_rm" class="rmlink" href="javascript: void(0)">X</a><br>\
                  </div>\
                </li>');

            $optioncontainer.append($option);
            
            if (title != undefined) {
                $('#id_o' + id +'_title').val(title);
            }
        
            $('#id_o' + id +'_rm').click({itemid: itemid, optionid: id}, removeOption);
        }

    }
    
    function removeOption(event){
        var count = $('#id_i' + event.data.itemid +'_optioncontainer').children().length;
        if (count>2) {        
            $('#o' + event.data.optionid ).remove()
        }
        updateOptionTitles(event);
    }   
    
    function updateOptionTitles(event) {
        $('#id_i' + event.data.itemid +'_optioncontainer > li').each(function(i) {
            $(this).find('label[for$="_title"]').text('Відповідь '+ (i+1));
        });
    }
    
    function onTypeChange(event){
        var type = $('#id_i' + event.data.id +'_type').val();
        $optioncontainer = $('#id_i' + event.data.id +'_optioncontainer');
                
        if (type == 'free') {
            $('#div_id_i' + event.data.id +'_addoption').hide();
            $optioncontainer.hide();
        } else {
            $('#div_id_i' + event.data.id +'_addoption').show();
            $optioncontainer.show();
        }
    }
    
    function getData(){
        var items = $('#itemcontainer').sortable('toArray');
        
        var data = new Array();    
        
        $('#itemcontainer > li').each(function(i) {
            var item_title = $(this).find('textarea').val();
            if (item_title != "") { //ignore empty item
                var item = new Object();
                item.title = item_title;
                item.type = $(this).find('select').val();
                if (item.type != 'free') {
                    item.options = new Array();
                    $(this).find('li').each(function(j) {
                        var option = $(this).find('input:text').val();
                        if (option != "") { //ignore empty option
                            item.options.push(option);
                        }
                    });
                }            
                data.push(item);
            }
        });
        return data;
    }
    
    function onSubmit(event) {
        var d = getData();
        if (d.length > 0) {
            $('#id_questions').val($.toJSON(d));
        } else {
            $('#id_questions').val('');
        }
        return true;
    }

  };
})( jQuery );
