function tinyDjangoBrowser(field_name, url, type, win) {
    var managerURL = '/admin/photofiler/photo/'

    tinyMCE.activeEditor.windowManager.open({
        file: managerURL,
        title: 'Кликните на эскиз нужной картинки',
        width: 800,
        height: 450,
        resizable: 'yes',
        inline: 'yes',
        close_previous: 'no',
        popup_css : false
    }, {
        window: win,
        input: field_name
    });

    return false;
}

$().ready(function() {
    var tinymceOptions = {
        script_url: '/site_media/static/js/tiny_mce/tiny_mce.js',

        mode : "specific_textareas",
        editor_selector : "mceEditor",
        
        theme: 'advanced',
        plugins: 'safari,pagebreak,layer,table,advhr,advimage,advlink,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras',

        theme_advanced_buttons1: 'bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect',
        theme_advanced_buttons2: 'search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor',
        theme_advanced_buttons3: 'tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,iespell,media,advhr,|,print,|,fullscreen',
        theme_advanced_buttons4: 'insertlayer,moveforward,movebackward,absolute,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,pagebreak',
        theme_advanced_toolbar_location: 'top',
        theme_advanced_toolbar_align: 'left',
        theme_advanced_statusbar_location: 'bottom',
        theme_advanced_resizing: true,

        // Drop lists for link/image/media/template dialogs
        template_external_list_url: 'lists/template_list.js',
        external_link_list_url: 'lists/link_list.js',
        external_image_list_url: 'lists/image_list.js',
        media_external_list_url: 'lists/media_list.js',

        doctype: '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
        content_css: '/media/css/admin/editor.css',

        file_browser_callback: 'tinyDjangoBrowser',
        convert_urls : false
    };
    
    tinyMCE.init(tinymceOptions)
    
    $('textarea#id_body').css({'width': '700px', 'height': '400px'});
    $('textarea#id_body').addClass('mceEditor');
    //$('textarea#id_body').tinymce(tinymceOptions);

});
