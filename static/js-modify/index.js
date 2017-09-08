require("../../bower_components/angular/angular.js");
require("../../bower_components/angular-animate/angular-animate.js");
jQuery = $ = require("../../bower_components/jquery/dist/jquery.js");
require("../../bower_components/AdminLTE/dist/js/app.min.js");
require("../../bower_components/bootstrap/dist/js/bootstrap.js");
Ctrl = angular.module('app',['ngAnimate']).controller('Ctrl',['$scope',function($scope){
    $scope.nav = 'live';
    $scope.logout = function() {
        jQuery.get("/sys/logout",function(data){
            location.href = "/admin/login";
        });
    };
    start = 0;
    limit = 20;
    $scope.page = 1;
    $scope.live_active = 'active';
    var refresh_type = function () {
        jQuery.get("/sys/get_types/",function (data) {
            $scope.types = data.data;
            $scope.type = $scope.types[0].id;
            $scope.$apply();
            refresh();
        });
    };
    refresh_type();
    var refresh = function() {
        option = {"start":start,"limit":limit};
        jQuery.get("/sys/get_data/?type="+$scope.type,option,function(data){
            $scope.data = data.data;
            $scope.$apply();
        });
        jQuery.get("/sys/get_total/?type="+$scope.type,function (data) {
            $scope.total = data.data;
            $scope.total.same = Math.floor(parseFloat($scope.total.same)*10000)/100;
            $scope.$apply();
        });
    };
    $scope.spider = function() {
        jQuery.get('/sys/spider/',function (data) {
            if(data.error != '0') {
                alert(data.data.message);
            }
        });
    };
    $scope.clear_weight = function () {
        jQuery.get('/sys/clear_weight/',function (data) {
            if(data.error_no == '0') {
                alert("清除成功");
                refresh();
            }
        });
    };
    $scope.download_xls_yesterday = function() {
        jQuery.get('/sys/download_excel_yesterday/?type='+$scope.type,function(data){
            window.open(data.data);
        })  ;
    };
    $scope.download_xls = function() {
        jQuery.get('/sys/download_excel/?type='+$scope.type,function(data){
            window.open(data.data);
        })  ;
    };
    $scope.download_total = function() {
        jQuery.get('/sys/download_total/?type='+$scope.type,function (data) {
           window.open(data.data) ;
        });
    };
    $scope.download_xls_title = function() {

        jQuery.get('/sys/download_xls_title/?type='+$scope.type,function (data) {
            window.open(data.data) ;
        });
    };
    $scope.select_type = function (id) {
        $scope.type = id;
        refresh();
    };
    $scope.change_weight = function() {
        jQuery.get('/sys/change_weight/',{
            'id' : $scope.view.id,
            'n' : $scope.weight
        },function (data) {
            if(data.error_no == '0') refresh();
        });
    };
    $scope.change_change = function() {
        jQuery.get('/sys/change_change/',{
            'id' : $scope.view.id,
            'n' : $scope.change
        },function (data) {
            if(data.error_no == '0') refresh();
        });
    };
    $scope.goToPage = function(page) {
        start = (page-1)*limit;
        $scope.page = page;
        refresh();
    };
    $scope.view = {};
    $scope.editForm = function(edit) {
        $scope.view = edit;
        $scope.weight = edit.weight;
        $scope.change = edit.change;
        for(var i=0;i<edit.title.length;i++) {
            for(var j=0;j<edit.op_title.length;j++) {
                if (edit.op_title[j].title == edit.title[i].title) {
                    $scope.view.title[i].same = '1';
                    $scope.view.op_title[j].same = '1';
                    break;
                }
            }
        }
    };
    $scope.delete_user = function () {
        jQuery.get('/sys/delete_user/?id='+$scope.view.id,function (data) {
            refresh();
        });
    }
    $scope.delete = function () {
        jQuery.get('/sys/delete_type/?id='+$scope.delete_type_id,function (data) {
            if(data.error_no == '0') {
                refresh_type();
            }
            else {
                alert(data.data.message);
            }
        })
    };
    $scope.upload = function() {
        formData = new FormData(jQuery('#upload-form')[0]);
        jQuery.ajax({
            url: '/sys/upload_data_resource/',
            type: "POST",
            data: formData,
            contentType : false,
            processData : false,
            success: function(data){
                refresh();
            }
        });
    };
    $scope.download = function () {
        jQuery.get('/sys/download_data_resource/?type='+$scope.type,function (data) {
            if(data.error_no == '0') {
                window.open(data.data);
            }
        }) ;
    };
    $scope.save = function() {
        jQuery.get("/sys/new_type/",$scope.obj,function(data){
            refresh_type();
        });
    };
}]);
Ctrl.$inject = ['$scope','Ctrl'];