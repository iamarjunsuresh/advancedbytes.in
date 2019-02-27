function fun(id)
{
$("#headline"+id).html($("#edit1"+id).val());
$("#content"+id).html($("#edit2"+id).val());




}

function fun2(id)
{

    itle=$("#edit1"+id).val();
    ontent=$("#edit2"+id).val();
    dat=$("#edit_date"+id).val();
    $.post( "/admin_edit", { title: itle, content:ontent,date:dat } );




}