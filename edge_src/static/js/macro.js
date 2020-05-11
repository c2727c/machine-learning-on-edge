function createLabel(slabelName,sText,sparaList) {
    var oLabel = new Object;
    oLabel.labelName = slabelName;
    oLabel.paraList = sparaList;
    oLabel.text = sText;
    oLabel.toString = function() {
        var s="<"+oLabel.labelName;
        for(var i=0;i<oLabel.paraList.length;++i){
            s+=" "+oLabel.paraList[i][0]+" = "+oLabel.paraList[i][1]+" ";
        }
        s+=">";
        s+=oLabel.text+"</"+oLabel.labelName+">";
        return s;
    };
    return oLabel;
};
function test(){alert();};
function creatTable(col_lists){
//检验至少有一个列表，检验其长度均相等
    var tableData=""
    var col_num = col_lists.length
    var row_num = col_lists[0].length
    for(var i=0;i<row_num;i++){
        var row="<tr>";
        for(var j = 0;j<col_num;j++){
            row += "<td>"+col_lists[j][i]+"</td>";
        }
        //最后一列添加按钮
        var label_o = createLabel("button","upload",
                                [["class","up_btn"],
                                ["id",col_lists[0][i]]]);
        row +="<td>"+label_o.toString()+"</td>";
        row+="</tr>";
        tableData+=row;



    }
    $("#tbody1").html(tableData);
};


