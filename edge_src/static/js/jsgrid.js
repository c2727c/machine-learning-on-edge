var datas = [
    { "id": "Connor Johnston", "title": '45', "is_active": '2'},
    { "id": "Lacey Hess", "title": '29', "is_active": '3'},
    { "id": "Timothy Henson", "title": '56', "is_active": '1'},
    { "id": "Ramona Benton", "title": '32', "is_active": '3'}
];

var clients = [
    { "Name": "Otto Clay", "Age": 25, "Country": 1, "Address": "Ap #897-1459 Quam Avenue", "Married": false },
    { "Name": "Connor Johnston", "Age": 45, "Country": 2, "Address": "Ap #370-4647 Dis Av.", "Married": true },
    { "Name": "Lacey Hess", "Age": 29, "Country": 3, "Address": "Ap #365-8835 Integer St.", "Married": false },
    { "Name": "Timothy Henson", "Age": 56, "Country": 1, "Address": "911-5143 Luctus Ave", "Married": true },
    { "Name": "Ramona Benton", "Age": 32, "Country": 3, "Address": "Ap #614-689 Vehicula Street", "Married": false }
];

var countries = [
    { Name: "", Id: 0 },
    { Name: "United States", Id: 1 },
    { Name: "Canada", Id: 2 },
    { Name: "United Kingdom", Id: 3 }
];

function setjsg(){
     $("#jsGrid").jsGrid({
        width: "100%",
        height: "400px",

        inserting: true,
        editing: true,
        sorting: true,
        paging: true,

        data: clients,

        fields: [
            { name: "FILENAME", type: "text", width: 150, validate: "required" },
            { name: "SIZE", type: "number", width: 50 },
            { name: "DATE", type: "text", width: 200 },
            { name: "ON EDGE", type: "select", items: countries, valueField: "Id", textField: "Name" },
            { name: "ON CLOUD", type: "checkbox", title: "Is Married", sorting: false },
            { type: "control" }
        ]
    });
}

var modelGridPara = {
    height: "auto",
    width: "100%",
    sorting: true,
    paging: true,
    autoload: true,
    pageSize: 10,
    pageButtonCount: 5,
    deleteConfirm: "Do you really want to delete your job listing?",
    controller: {
       loadData: function() {
           return $.get("/model/list");
       },
    },
    fields: [
        { name: "filename", title: "模型名称", type: "text", visible: true, width: 100 },
        { name: "size", title: "文件大小", type: "number", width: 100 },
        { name: "mtime",formatter:"date",
            formatoptions: {newformat:'Y-m-d'},title: "修改时间", width: 100 },
        { name: "status", type: "text", title: "同步状态", width: 100 },
        { name:"操作", type: "control", width: 100, editButton: true, deleteButton: false,
             itemTemplate: function(value, item) {
                var $result = jsGrid.fields.control.prototype.itemTemplate.apply(this, arguments);
                var $customButton1 = $("<button>")
                    .html('下载')
                    .click(function(e) {
                    $.get("/model/download?fname="+item.filename);
                    alert("ID: " + item.filename);
                    e.stopPropagation();
                });
//               var $customButton2 = $("<button>")
//                    .attr("class","train_btn")
//                    .html('训练')
//                    .click(function(e) {
//                        alert("ID: " + item.filename);
//                        e.stopPropagation();
//                    });
               var $customButton3 = $("<button>")
                    .html('设为当前')
                    .click(function(e) {
                       alert("ID: " + item.filename);
                       $.get("/setting/setconfig?value="+item.filename+
                       "&name=CURRENT_MODEL")
                       e.stopPropagation();
                    });
                return $("<div>")
                        .append($customButton1)
//                        .append($customButton2)
                        .append($customButton3);
            },
        }
    ]
};

var dataGridPara = {
    height: "auto",
    width: "100%",
    sorting: true,
    paging: true,
    autoload: true,
    pageSize: 10,
    pageButtonCount: 5,
    deleteConfirm: "Do you really want to delete your job listing?",
    controller: {
       loadData: function() {
           return $.get("/data/list");
       },
    },
    fields: [
        { name: "filename", title: "模型名称", type: "text", visible: true, width: 100 },
        { name: "size", title: "文件大小", type: "number", width: 100 },
        { name: "mtime",formatter:"date",
            formatoptions: {newformat:'Y-m-d'},title: "修改时间", width: 100 },
        { name: "status", type: "text", title: "同步状态", width: 100 },
        { name:"操作", type: "control", width: 100, editButton: true, deleteButton: false,
             itemTemplate: function(value, item) {
                var $result = jsGrid.fields.control.prototype.itemTemplate.apply(this, arguments);
                var $customButton1 = $("<button>")
                    .html('上传')
                    .click(function(e) {
                    $.get("/data/upload_to_cloud?fname="+item.filename)
                    alert("ID: " + item.filename);
                    e.stopPropagation();
                });
               var $customButton2 = $("<button>")
                    .html('训练')
                    .attr("class","train_btn")
                    .click(function(e) {
                       alert("ID:" + item.filename);
                       $("#background").show();
                       $("#input_id").val(item.filename);
                       e.stopPropagation();
                    });
               var $customButton3 = $("<button>")
                    .html('设为当前')
                    .click(function(e) {
                       alert("ID: " + item.filename);
                       $.get("/setting/setconfig?value="+item.filename+
                       "&name=DATASET_COLLECTING_CSV")
                       e.stopPropagation();
                    });
                return $("<div>")
                        .append($customButton1)
                        .append($customButton2)
                        .append($customButton3);
            },
        }
    ]
};


function setjsg2(){
    $("#jsGrid").jsGrid(modelGridPara);
}

function setjsg_data(){
    $("#jsGrid").jsGrid(dataGridPara);
}

